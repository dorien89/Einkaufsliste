import os
import json
import asyncio
from flask import Blueprint, jsonify, request, current_app

bp = Blueprint('bring', __name__, url_prefix='/api/bring')

CONFIG_FILE = os.path.join(
    os.path.abspath(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))),
    'database', 'bring_config.json'
)

def _load_config():
    if not os.path.exists(CONFIG_FILE):
        return {'email': '', 'password': '', 'list_name': ''}
    with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def _save_config(cfg):
    with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
        json.dump(cfg, f, ensure_ascii=False, indent=2)


@bp.route('/config', methods=['GET'])
def get_config():
    cfg = _load_config()
    # Never return the password to the client
    return jsonify({'email': cfg.get('email', ''), 'list_name': cfg.get('list_name', ''),
                    'has_password': bool(cfg.get('password', ''))})


@bp.route('/config', methods=['POST'])
def save_config():
    data = request.get_json()
    cfg = _load_config()
    if 'email' in data:
        cfg['email'] = data['email'].strip()
    if 'list_name' in data:
        cfg['list_name'] = data['list_name'].strip()
    if data.get('password', '').strip():
        cfg['password'] = data['password'].strip()
    _save_config(cfg)
    return jsonify({'success': True})


@bp.route('/push', methods=['POST'])
def push_to_bring():
    try:
        from bring_api import Bring
    except ImportError:
        return jsonify({'error': 'bring-api ist nicht installiert. Bitte `pip install bring-api` ausführen.'}), 500

    cfg = _load_config()
    email = cfg.get('email', '').strip()
    password = cfg.get('password', '').strip()
    list_name = cfg.get('list_name', '').strip()

    if not email or not password:
        return jsonify({'error': 'Bring! E-Mail und Passwort fehlen. Bitte in den Einstellungen eintragen.'}), 400

    # Items come from the request body (sent by the client, already filtered for at-home)
    data = request.get_json() or {}
    items = data.get('items', [])  # [{name, amount, unit}, ...]

    if not items:
        return jsonify({'error': 'Keine Artikel zum Übertragen.'}), 400

    async def _push():
        import aiohttp
        async with aiohttp.ClientSession() as session:
            bring = Bring(session, email, password)
            await bring.login()
            lists_data = await bring.loadLists()
            bring_lists = lists_data.get('lists', [])
            if not bring_lists:
                raise RuntimeError('Keine Bring!-Listen gefunden.')

            # Find by name, fall back to first list
            target = next((l for l in bring_lists if l.get('name', '').lower() == list_name.lower()), None)
            if target is None:
                target = bring_lists[0]

            list_uuid = target['listUuid']

            for item in items:
                name = item['name']
                a = item.get('amount', '')
                u = item.get('unit', '')
                # Format specification like "500 g" or "3 Stück"
                if a and u:
                    try:
                        a_val = float(a)
                        spec = f"{int(a_val) if a_val == int(a_val) else round(a_val, 1)} {u}".strip()
                    except (ValueError, TypeError):
                        spec = f"{a} {u}".strip()
                else:
                    spec = ''
                await bring.saveItem(list_uuid, name, spec)

            return target.get('name', list_uuid)

    try:
        list_name_used = asyncio.run(_push())
        return jsonify({'success': True, 'list': list_name_used, 'count': len(items)})
    except Exception as e:
        return jsonify({'error': str(e)}), 500
