from flask import Flask, render_template, request, redirect, url_for
import json
import folium
import psycopg2
from psycopg2.extras import DictCursor
from folium.plugins import MarkerCluster
import requests
from requests.auth import HTTPBasicAuth

app = Flask(__name__)

def parse_app_version(app_version):
    """Parse app version string into components."""
    parts = app_version.split('_')
    if len(parts) != 3:
        return None
    
    version = parts[2]
    build_number = ''
    
    if '(' in version:
        version_parts = version.split('(')
        version = version_parts[0]
        build_number = f"({version_parts[1]}"
    
    return {
        'app_name': parts[0],
        'platform': parts[1],
        'version': version,
        'build_number': build_number
    }

def get_task_list():
    """Return list of predefined tasks."""
    return [
        {
            "summary": "Wykonanie testów regresji aplikacji {app_name} {platform} w wersji {version}",
            "description": "Wykonanie testów regresji aplikacji {app_name} {platform} w wersji {version}.",
            "issuetype": "10012",
            "dynamic_title": True
        },
        {
            "summary": "[QA] - Testy eksploracyjne oraz smoke testy iteracja {iteration}",
            "description": "Testy eksploracyjne oraz smoke testy",
            "issuetype": "10002",
            "dynamic_title": False
        },
        {
            "summary": "[QA] - Testy urządzeń BS iteracja {iteration}",
            "description": "Testy urządzeń BS: dodawanie urządzenia, edycja, usuwanie, lokalizacja, historia lokalizacji, SOS, połączenia, budzik, kontakty, nasłuch, shareing lokalizacji, oszczędzanie baterii, automatyczna lokalizacja",
            "issuetype": "10002",
            "dynamic_title": False
        },
        {
            "summary": "[QA] - Testy urządzeń BZ iteracja {iteration}",
            "description": "Testy urządzeń BZ: dodawanie urządzenia, edycja, usuwanie, lokalizacja, historia lokalizacji, SOS, połączenia, nasłuch, shareing lokalizacji, oszczędzanie baterii, automatyczna lokalizacja",
            "issuetype": "10002",
            "dynamic_title": False
        },
        {
            "summary": "[QA] - Testy urządzeń GJD iteracja {iteration}",
            "description": "Testy urządzeń GJD: dodawanie urządzenia, edycja, usuwanie, lokalizacja, historia lokalizacji, SOS, połączenia, budzik, kontakty, czat, shareing lokalizacji, oszczędzanie baterii, automatyczna lokalizacja",
            "issuetype": "10002",
            "dynamic_title": False
        },
        {
            "summary": "[QA] - Testy ochrony rodzicielskiej iteracja {iteration}",
            "description": "Testy związane z bliskim, dla którego została uruchomiona ochrona rodzicielska (BSF).",
            "issuetype": "10002",
            "dynamic_title": False
        },
        {
            "summary": "[QA] - Testy funkcjonalności przypomnienia o lekach iteracja {iteration}",
            "description": "Testy funkcjonalności przypomnienia o lekach.",
            "issuetype": "10002",
            "dynamic_title": False
        },
        {
            "summary": "[QA] - Testy funkcjonalności karty zdrowia iteracja {iteration}",
            "description": "Testy ciśnienia, saturacji, temperatury, czujnika upadku.",
            "issuetype": "10002",
            "dynamic_title": False
        },
        {
            "summary": "[QA] - Testy autologowania dla różnych sieci iteracja {iteration}",
            "description": "Testy autologowania dla sieci Play, Orange, Plus, TMobile",
            "issuetype": "10002",
            "dynamic_title": False
        },
        {
            "summary": "[QA] - Testy pakietów iteracja {iteration}",
            "description": "Testy kupowania pakietów, weryfikacji limitów dla danego pakietu.",
            "issuetype": "10002",
            "dynamic_title": False
        },
        {
            "summary": "[QA] - Testy stref iteracja {iteration}",
            "description": "Testy dodawania, usuwania i edycji stref.",
            "issuetype": "10002",
            "dynamic_title": False
        },
        {
            "summary": "[QA] - Testy weryfikacji elementów na ekranie udostępniania lokalizacji iteracja {iteration}",
            "description": "Weryfikacja długości czasu oraz wiadomości udostępniania lokalizacji.",
            "issuetype": "10002",
            "dynamic_title": False
        },
        {
            "summary": "[QA] - Testy związane z Bliskim iteracja {iteration}",
            "description": "Testy związane z Bliskim: dodawanie, usuwanie, edycja, SOS, lokalizacja, historia lokalizacji, shareing lokalizacji",
            "issuetype": "10002",
            "dynamic_title": False
        },
        {
            "summary": "[QA] - Testy związane z HomeWiFi iteracja {iteration}",
            "description": "Testy związane z HomeWiFi.",
            "issuetype": "10002",
            "dynamic_title": False
        },
        {
            "summary": "[QA] - Testy Pakiet Family iteracja {iteration}",
            "description": "Opis: https://jiralocon.atlassian.net/wiki/spaces/LOCON/pages/1517879312/Pakiet+Family",
            "issuetype": "10002",
            "dynamic_title": False
        },
        {
            "summary": "[QA] - Testy wideo rozmów dla urządzeń GJD iteracja {iteration}",
            "description": "Testy związane z wideorozmowami dla urządzeń GJD",
            "issuetype": "10002",
            "dynamic_title": False
        },
        {
            "summary": "[QA] - Testy pushy/deeplinków iteracja {iteration}",
            "description": "Testy pushy/deeplinków.",
            "issuetype": "10002",
            "dynamic_title": False
        },
        {
            "summary": "[QA] - Testy funkcjonalności przyznawania prezentów - iteracja {iteration}",
            "description": "Opis: https://jiralocon.atlassian.net/wiki/spaces/LOCON/pages/1575976961/Poprawa+ocen+aplikacji",
            "issuetype": "10002",
            "dynamic_title": False
        },
        {
            "summary": "[QA] - Testy funkcjonalności ZST iteracja {iteration}",
            "description": "Testy związane z funkcjonalnością Znajdź Swój Telefon: https://jiralocon.atlassian.net/wiki/spaces/LOCON/pages/1623359489/ZNAJD+SW+J+TELEFON",
            "issuetype": "10002",
            "dynamic_title": False
        },
        {
            "summary": "[QA] - Testy funkcjonalności StopHejt iteracja {iteration}",
            "description": "Testy związane z funkcjonalnością StopHejt: https://jiralocon.atlassian.net/wiki/spaces/LOCON/pages/1649737729/STOP+HEJT",
            "issuetype": "10002",
            "dynamic_title": False
        },
        {
            "summary": "[QA] - Testy przyznawania promocji iteracja {iteration}",
            "description": "Weryfikacja przyznawania promocji dla różnych sieci: TMPL, OPL, PLK, P4.",
            "issuetype": "10002",
            "dynamic_title": False
        },
        {
            "summary": "[QA] - Testy zbierania adresów email iteracja {iteration}",
            "description": "Weryfikacja zbierania adresów email.",
            "issuetype": "10002",
            "dynamic_title": False
        },
        {
            "summary": "[QA] - Testy elementów na mapie - alerty i statusy teleopieki iteracja {iteration}",
            "description": "Weryfikacja elementów na mapie - alerty i statusy teleopieki.",
            "issuetype": "10002",
            "dynamic_title": False
        }
    ]

def create_task(summary, description, project_key, issuetype, epic_id, app_version, sprint):
    """Create a JIRA task with the given parameters."""
    try:
        url = 'https://jiralocon.atlassian.net/rest/api/3/issue/'
        
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json"
        }
        
        payload = json.dumps({
            "update": {},
            "fields": {
                "summary": summary,
                "issuetype": {
                    "id": issuetype
                },
                "project": {
                    "id": project_key
                },
                "description": {
                    "type": "doc",
                    "version": 1,
                    "content": [
                        {
                            "type": "paragraph",
                            "content": [
                                {
                                    "text": description,
                                    "type": "text"
                                }
                            ]
                        }
                    ]
                },
                "priority": {
                    "id": "3"
                },
                "customfield_10014": epic_id,
                "customfield_10034": [{
                    "name": app_version
                }],
                "customfield_10020": sprint
            }
        })
        
        response = requests.post(
            url, 
            headers=headers, 
            data=payload, 
            auth=HTTPBasicAuth('dawid.hawryluk@locon.pl', 'Bn47hMxgmZ79Rl9qOBub2744'),
            timeout=10
        )
        
        return response.status_code == 201
            
    except Exception:
        return False

# Function to establish a database connection
def get_db_connection():
    return psycopg2.connect(
        dbname='gjd', 
        user='usr_internal_tools',
        password='TcdfQkSkcA6VurChE3eumBAoX!',
        host='br-db.locon-internal.net'
    )

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        app_version = request.form['app_version']
        epic_id = request.form['epic_id']
        iteration_number = request.form['iteration_number']
        sprint = int(request.form['sprint'])
        
        # Parse app version
        version_info = parse_app_version(app_version)
        
        selected_tasks = request.form.getlist('tasks')
        task_list = get_task_list()
        
        success_count = 0
        failed_count = 0
        
        for task_id in selected_tasks:
            task = task_list[int(task_id)]
            
            # Handle dynamic title if needed
            if task.get('dynamic_title'):
                summary = task['summary'].format(
                    app_name=version_info['app_name'],
                    platform=version_info['platform'],
                    version=version_info['version']
                )
                description = task['description'].format(
                    app_name=version_info['app_name'],
                    platform=version_info['platform'],
                    version=version_info['version']
                )
            else:
                summary = task['summary'].replace('{iteration}', iteration_number)
                description = task['description']
            
            if create_task(
                summary=summary,
                description=description,
                project_key="10001",
                issuetype=task['issuetype'],
                epic_id=epic_id,
                app_version=app_version,
                sprint=sprint
            ):
                success_count += 1
            else:
                failed_count += 1
        
        if failed_count == 0:
            return redirect('/?success=true')
        elif success_count == 0:
            return redirect('/?error=true')
        else:
            return redirect(f'/?partial=true&success={success_count}&failed={failed_count}')

    return render_template('index.html', tasks=get_task_list())

@app.route('/map_form')
def map_form():
    return render_template('generowanie_mapy.html')

@app.route('/submit_form', methods=['POST'])
def submit_form():
    # Extracting form data
    parentNumber = request.form.get('parentNumber')
    childNumber = request.form.get('childNumber')
    startDate = request.form.get('startDate', None)  # Optional
    endDate = request.form.get('endDate', None)  # Optional
    startDate2 = request.form.get('startDate2', None)  # Optional
    endDate2 = request.form.get('endDate2', None)  # Optional
    imeiNumber = request.form.get('imeiNumber', None)  # Get imeiNumber, default to None if not present
    createAreas = 'createAreasCheckbox' in request.form
    form_data = request.form.to_dict()
    non_null_params = {key: value for key, value in form_data.items() if value}
    # Redirecting to the map generation page with the form data
    return redirect(url_for('generate_map', **non_null_params))

@app.route('/map')
def generate_map():
    # Retrieving query parameters
    parentNumber = request.args.get('parentNumber')
    childNumber = request.args.get('childNumber')
    startDate = request.args.get('startDate', None)  # Optional
    endDate = request.args.get('endDate', None)  # Optional
    startDate2 = request.args.get('startDate2', None)  # Optional
    endDate2 = request.args.get('endDate2', None)  # Optional
    imeiNumber = request.args.get('imeiNumber', None)  # Optional
    createAreas = 'createAreasCheckbox' in request.args

    # Example of database usage (adjust SQL query as needed)
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=DictCursor)
    if imeiNumber:  # If imeiNumber is not None and not an empty string
        query = """
        SELECT * FROM pgps.tracker_status ts
        INNER JOIN pgps.tracker t ON ts.device_id = t.id
        WHERE t.imei = %s AND valid = 'true'
        """
        params = [imeiNumber]
    else:
        query = """
        select msl.* from gjd.mobile_station_location msl 
        inner join gjd.mobile_station ms ON msl.mobilestation_id = ms.id 
        inner join gjd.users u ON u.id = ms.user_id
        where ms.msid=%s
        and u.phone = %s
        and resulttype='OK'
        """
        params = [childNumber, parentNumber]

    if startDate and endDate:
        startDate = startDate.replace("T", " ")
        endDate = endDate.replace("T", " ")
        query += " AND time >= %s and time <= %s"
        params += [startDate, endDate]

    if startDate2 and endDate2:
        startDate2 = startDate2.replace("T", " ")
        endDate2 = endDate2.replace("T", " ")
        query += " AND location_time >= %s and location_time <= %s"
        params += [startDate2, endDate2]

    query += " order by 1 desc LIMIT 100"
    cur.execute(query, params)
    rows = cur.fetchall()
    conn.close()
    
    folium_map = folium.Map(location=[53.4066208,14.5341284], zoom_start=12)

    createAreas = request.args.get('createAreasCheckbox')
    if createAreas:
        # Connect to the database
        conn = get_db_connection()
        cur = conn.cursor(cursor_factory=DictCursor)
        
        # Fetch areas data from the database
        if imeiNumber:
            query = """
            SELECT up.* FROM gjd.user_poi up
            INNER JOIN pgps.tracker t ON up.user_id = t.user_id
            WHERE t.imei = %s AND up.status = 'STATUS_ACTIVE' LIMIT 100
            """
            params = [imeiNumber]
        else:
            query = """
            SELECT * FROM gjd.user_poi up
            INNER JOIN gjd.users us ON up.user_id = us.id
            WHERE us.phone = %s AND status = 'STATUS_ACTIVE' LIMIT 100
            """
            params = [parentNumber]

        cur.execute(query, params)
        areas = cur.fetchall()
        
        # For each area, draw a circle on the map using Folium
        for area in areas:
            lon, lat = map(float, area['area_definition'].replace('POINT (', '').replace(')', '').split())
            popup_message = f"Nazwa: {area['name']}<br>Wielkosc: {area['radius']}m"
            folium.Circle(
                location=(lat, lon),
                radius=area['radius'],  # Radius in meters
                popup=popup_message,  # Name of the area as popup
                color='crimson',
                fill=True,
                fill_color='crimson'
            ).add_to(folium_map)
        
        cur.close()
        conn.close()

    # Initialize Folium map
    marker_cluster = MarkerCluster().add_to(folium_map)
    # Add markers for each row in the query result
    for row in rows:
        if row['type'] == 'GSM':
            color = 'red'
        elif row['type'] == 'NETWORK':
            color = 'red'
        elif row['type'] == 'WIFI':
            color = 'blue'
        elif row['type'] == 'GPS':
            color = 'blue'
        else:
            color = 'green'  # Default color for unspecified types
    
        if imeiNumber:
            time = row['location_time']
        else:
            time = row['time']

        popup_message = f"Czas: {time}<br>Wspolrzedne: {row['lat'], row['lon']}<br>Typ: {row['type']}"
        folium.Marker(
            [row['lat'], row['lon']], 
            popup=popup_message,
            icon=folium.Icon(color=color, icon='home')
        ).add_to(marker_cluster)
    
    folium_map.fit_bounds(folium_map.get_bounds())

    # Get the map HTML components
    map_html = folium_map._repr_html_()
    map_script = folium_map.get_root().script.render()
    map_css = folium_map.get_root().header.render()

    # Render the template with the map components
    return render_template('map_template.html', 
                         folium_map=map_html,
                         folium_js=map_script,
                         folium_css=map_css)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=50001, debug=False) 