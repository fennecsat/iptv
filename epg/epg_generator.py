import requests
import json
import xml.etree.ElementTree as ET
from xml.dom import minidom
from datetime import datetime, timedelta
import pytz
from bs4 import BeautifulSoup
import time

# Constants
OUTPUT_FILE = 'epg.xml'
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

def prettify(elem):
    """Return a pretty-printed XML string for the Element."""
    rough_string = ET.tostring(elem, 'utf-8')
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="  ")

def get_shahid_epg():
    """Fetch Shahid EPG data."""
    today = datetime.now(pytz.utc)
    yesterday = today - timedelta(days=1)
    tomorrow = today + timedelta(days=1)
    
    shahid_from = yesterday.strftime('%Y-%m-%dT23:00:00.000Z')
    shahid_to = tomorrow.strftime('%Y-%m-%dT22:59:59.999Z')
    
    shahid_channel_ids = '400924,400921,400917,387248,387251,49923122575716,387290,387937,400919,387293,387296,409387,387294,418308,986064,986069,387286,1003218,387288,862837,997605,1001845,999399,414449,409385,409390,989622'
    url = f"https://api3.shahid.net/proxy/v2.1/shahid-epg-api/?csvChannelIds={shahid_channel_ids}&language=en&from={shahid_from}&to={shahid_to}"
    
    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        return response.json() if response.status_code == 200 else {'items': []}
    except:
        return {'items': []}

def get_shahid_channel_map():
    """Return Shahid channel mapping."""
    return {
        # Documentary Channels
        '997605': {'name': 'Asharq Documentary', 'tvg_id': 'AsharqDocumentary.sa'},
        '1001845': {'name': 'Asharq Discovery', 'tvg_id': 'AsharqDiscovery.sa'},
        '999399': {'name': 'Nature Time', 'tvg_id': 'NatureTime.sa'},
        # MBC Channels
        '387248': {'name': 'MBC1', 'tvg_id': 'MBC1.sa'},
        '400917': {'name': 'MBC2', 'tvg_id': 'MBC2.sa'},
        '409385': {'name': 'MBC3', 'tvg_id': 'MBC3.sa'},
        '400919': {'name': 'MBC4', 'tvg_id': 'MBC4.sa'},
        '387937': {'name': 'MBC5', 'tvg_id': 'MBC5.sa'},
        '400921': {'name': 'MBC Action', 'tvg_id': 'MBCAction.sa'},
        '400924': {'name': 'MBC Max', 'tvg_id': 'MBCMax.sa'},
        '387251': {'name': 'MBC Drama', 'tvg_id': 'MBCDrama.sa'},
        '387296': {'name': 'MBC+ Drama', 'tvg_id': 'MBCPlusDrama.sa'},
        '49923122575716': {'name': 'MBC Masr Drama', 'tvg_id': 'MBCMasrDrama.sa'},
        '387290': {'name': 'MBC Masr', 'tvg_id': 'MBCMasr.sa'},
        '387293': {'name': 'MBC Masr 2', 'tvg_id': 'MBCMasr2.sa'},
        '387294': {'name': 'MBC Iraq', 'tvg_id': 'MBCIraq.sa'},
        '409387': {'name': 'MBC Bollywood', 'tvg_id': 'MBCBollywood.sa'},
        '418308': {'name': 'MBC Persia', 'tvg_id': 'MBCPersia.sa'},
        '414449': {'name': 'Wanasah', 'tvg_id': 'Wanasah.sa'},
        # Movies Channels
        '986064': {'name': 'Movies Action', 'tvg_id': 'MoviesAction.sa'},
        '986069': {'name': 'Movies Thriller', 'tvg_id': 'MoviesThriller.sa'},
        '989622': {'name': 'Aflam', 'tvg_id': 'Aflam.sa'},
        # News Channels
        '387286': {'name': 'Al Arabiya', 'tvg_id': 'AlArabiya.sa'},
        '1003218': {'name': 'Al Arabiya Business', 'tvg_id': 'AlArabiyaBusiness.sa'},
        '387288': {'name': 'Al Hadath', 'tvg_id': 'AlHadath.sa'},
        '862837': {'name': 'Asharq News', 'tvg_id': 'AsharqNews.sa'},
        # Kids Channels
        '409390': {'name': 'Spacetoon', 'tvg_id': 'Spacetoon.sa'},
    }

def get_adtv_epg():
    """Fetch ADTV EPG data."""
    url = 'https://adtv.ae/api/biz/program/list'
    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        return response.json() if response.status_code == 200 else {'response': []}
    except:
        return {'response': []}

def get_adtv_channel_map():
    """Return ADTV channel mapping."""
    return {
        'Abu Dhabi Channel': {'name': 'Abu Dhabi TV', 'tvg_id': 'AbuDhabiTV.ae'},
        'Emirates Channel': {'name': 'Al Emarat TV', 'tvg_id': 'EmiratesTV.ae'},
        'Baynounah': {'name': 'Baynounah TV', 'tvg_id': 'BaynounahTV.ae'},
        'National Geographic HD Channel': {'name': 'National Geographic Abu Dhabi', 'tvg_id': 'NationalGeographicAbuDhabi.ae'},
        'Majid Children Channel': {'name': 'Majid TV', 'tvg_id': 'MajidTV.ae'},
        'Abu Dhabi Sports Channel 1': {'name': 'Abu Dhabi Sports 1', 'tvg_id': 'AbuDhabiSports1.ae'},
        'Abu Dhabi Sports Channel 2': {'name': 'Abu Dhabi Sports 2', 'tvg_id': 'AbuDhabiSports2.ae'},
        'YAS Sports Channel': {'name': 'Yas TV', 'tvg_id': 'YasTV.ae'}
    }

def get_atlaspro_epg():
    """Fetch AtlasPro EPG data."""
    url = 'http://apbest.re/xmltv.php'
    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        if response.status_code == 200:
            root = ET.fromstring(response.content)
            programmes = []
            for programme in root.findall('programme'):
                programmes.append({
                    'channel_id': programme.get('channel'),
                    'start': programme.get('start'),
                    'stop': programme.get('stop'),
                    'title': programme.find('title').text if programme.find('title') is not None else '',
                    'desc': programme.find('desc').text if programme.find('desc') is not None else None,
                    'icon': programme.find('icon').get('src') if programme.find('icon') is not None else None
                })
            return programmes
    except:
        pass
    return []

def get_atlaspro_channel_map():
    """Return AtlasPro channel mapping."""
    return {
        # Channels from AtlasPro
        'TF1.fr': {'name': 'TF1', 'tvg_id': 'TF1.fr'},
        'tf1.fr': {'name': 'TF1', 'tvg_id': 'TF1.fr'},
        'TMC.fr': {'name': 'TMC', 'tvg_id': 'TMC.fr'},
        'tmc.fr': {'name': 'TMC', 'tvg_id': 'TMC.fr'},
        'TFX.fr': {'name': 'TFX', 'tvg_id': 'TFX.fr'},
        'tfx.fr': {'name': 'TFX', 'tvg_id': 'TFX.fr'},
        'LCI.fr': {'name': 'LCI', 'tvg_id': 'LCI.fr'},
        'lci.fr': {'name': 'LCI', 'tvg_id': 'LCI.fr'},
        'TF1SeriesFilms.fr': {'name': 'TF1 Séries Films', 'tvg_id': 'TF1SeriesFilms.fr'},
        'tf1seriesfilms.fr': {'name': 'TF1 Séries Films', 'tvg_id': 'TF1SeriesFilms.fr'},
        'ARTE.fr': {'name': 'Arte', 'tvg_id': 'ARTE.fr'},
        'arte.fr': {'name': 'Arte', 'tvg_id': 'Arte.fr'},
        'LEquipe.fr': {'name': 'L\'Équipe', 'tvg_id': 'LEquipe.fr'},
        'lequipe.fr': {'name': 'L\'Équipe', 'tvg_id': 'LEquipe.fr'},

        'france2.fr': {'name': 'France 2', 'tvg_id': 'France2.fr'},
        'france3.fr': {'name': 'France 3', 'tvg_id': 'France3.fr'},
        'france5.fr': {'name': 'France 5', 'tvg_id': 'France5.fr'},
        'france4.fr': {'name': 'France 4', 'tvg_id': 'France4.fr'},
        'M6.fr': {'name': 'M6', 'tvg_id': 'M6.fr'},
        'm6.fr': {'name': 'M6', 'tvg_id': 'M6.fr'},
        '6ter.fr': {'name': '6ter', 'tvg_id': '6ter.fr'},
        'W9.fr': {'name': 'W9', 'tvg_id': 'W9.fr'},
        'w9.fr': {'name': 'W9', 'tvg_id': 'W9.fr'},

        'CanalPlus.fr': {'name': 'Canal+', 'tvg_id': 'CanalPlus.fr'},
        'CNews.fr': {'name': 'CNews', 'tvg_id': 'CNews.fr'},
        'cnews.fr': {'name': 'CNews', 'tvg_id': 'CNews.fr'},
        'CStar.fr': {'name': 'CStar', 'tvg_id': 'CStar.fr'},
        'cstar.fr': {'name': 'CStar', 'tvg_id': 'CStar.fr'},
        'Cherie25.fr': {'name': 'Chérie 25', 'tvg_id': 'Cherie25.fr'},
        'cherie25.fr': {'name': 'Chérie 25', 'tvg_id': 'Cherie25.fr'},
        'Gulli.fr': {'name': 'Gulli', 'tvg_id': 'Gulli.fr'},
        'gulli.fr': {'name': 'Gulli', 'tvg_id': 'Gulli.fr'},
        
        'rmcdecouverte.fr': {'name': 'RMC Découverte', 'tvg_id': 'RMCDecouverte.fr'},
        'rmcstory.fr': {'name': 'RMC Story', 'tvg_id': 'RMCStory.fr'},
        'RMCStory.fr': {'name': 'RMC Story', 'tvg_id': 'RMCStory.fr'},
        'bfmtv.fr': {'name': 'BFM TV', 'tvg_id': 'BFMTV.fr'},
        'BFMTV.fr': {'name': 'BFM TV', 'tvg_id': 'BFMTV.fr'},

        'TV5MondeMaghrebOrient.fr': {'name': 'TV5Monde Maghreb-Orient', 'tvg_id': 'TV5MondeMaghrebOrient.fr'},
        'TV5MondeInfo.fr': {'name': 'TV5Monde Info', 'tvg_id': 'TV5MondeInfo.fr'},
        'TV5Style.fr': {'name': 'TV5Monde Style', 'tvg_id': 'TV5MondeStyle.fr'},
        'Tivi5.fr': {'name': 'TiVi5Monde', 'tvg_id': 'TiVi5Monde.fr'},

        'ViaGrandParis.fr': {'name': 'Le Figaro TV', 'tvg_id': 'LeFigaroTV.fr'},
        'france24.fr': {'name': 'France 24 Français', 'tvg_id': 'France24.fr'},
        'france24.uk': {'name': 'France 24 English', 'tvg_id': 'France24English.fr'},
        'aljazeera.uk': {'name': 'Al Jazeera English', 'tvg_id': 'AlJazeeraEnglish.qa'},
        'bbcarabiccanada.ca': {'name': 'BBC News Arabic', 'tvg_id': 'BBCNewsArabic.uk'},
        'bbcnews.uk': {'name': 'BBC News English', 'tvg_id': 'BBCNews.uk'},
        'skynews.uk': {'name': 'Sky News English', 'tvg_id': 'SkyNews.uk'},
    }

def fetch_alkass_day_data(day):
    """Fetch AlKass EPG data for a specific day."""
    url = "https://www.alkass.net/tvguide" + ("?day=next" if day == 'next' else "")
    
    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        if response.status_code != 200:
            return {}
            
        soup = BeautifulSoup(response.text, 'html.parser')
        qatar_tz = pytz.timezone('Asia/Qatar')
        current_date = datetime.now(qatar_tz)
        
        if day == 'next':
            current_date += timedelta(days=1)
            
        data = {}
        channel_names = ['one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'online']
        
        for i in range(1, 10):
            channel_key = f'alkass_{channel_names[i-1]}'
            data[channel_key] = []
            
            channel_div = soup.find('ul', id=f'cg{i}')
            if not channel_div:
                continue
                
            programs = channel_div.find_all('tr')
            for program in programs:
                time_cell = program.find('td', class_='tv-prog-time')
                name_cell = program.find('td', class_='tv-prog-name')
                
                if time_cell and name_cell:
                    time_str = time_cell.get_text(strip=True)
                    name = name_cell.get_text(strip=True)
                    
                    try:
                        hour, minute = map(int, time_str.split(':'))
                        program_time = current_date.replace(hour=hour, minute=minute, second=0, microsecond=0)
                        program_time = qatar_tz.localize(program_time) if program_time.tzinfo is None else program_time
                        
                        data[channel_key].append({
                            'start': program_time.strftime('%Y-%m-%d %H:%M:%S'),
                            'title': name
                        })
                    except:
                        continue
                        
        return data
    except:
        return {}

def get_alkass_epg():
    """Get AlKass EPG data for today and tomorrow."""
    qatar_tz = pytz.timezone('Asia/Qatar')
    today_data = fetch_alkass_day_data('today')
    tomorrow_data = fetch_alkass_day_data('next')
    
    # Combine data
    combined = {}
    channel_names = ['one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'online']
    
    for name in channel_names:
        channel_key = f'alkass_{name}'
        combined[channel_key] = (today_data.get(channel_key, []) + 
                                tomorrow_data.get(channel_key, []))
    
    return combined

def get_alkass_channel_map():
    """Return AlKass channel mapping."""
    return {
        'alkass_one': {
            'name': 'Alkass One',
            'tvg_id': 'AlkassOne.qa',
        },
        'alkass_two': {
            'name': 'Alkass Two',
            'tvg_id': 'AlkassTwo.qa',
        },
        'alkass_three': {
            'name': 'Alkass Three',
            'tvg_id': 'AlkassThree.qa',
        },
        'alkass_four': {
            'name': 'Alkass Four',
            'tvg_id': 'AlkassFour.qa',
        },
        'alkass_five': {
            'name': 'Alkass Five',
            'tvg_id': 'AlkassFive.qa',
        },
        'alkass_six': {
            'name': 'Alkass Six',
            'tvg_id': 'AlkassSix.qa',
        },
        'alkass_seven': {
            'name': 'Alkass Seven',
            'tvg_id': 'AlkassSeven.qa',
        },
        'alkass_eight': {
            'name': 'Alkass Eight',
            'tvg_id': 'AlkassEight.qa',
        },
        'alkass_online': {
            'name': 'Alkass SHOOF',
            'tvg_id': 'AlkassSHOOF.qa',
        }
    }

def generate_epg():
    """Generate the EPG XML file."""
    print("Fetching EPG data from all sources...")
    
    # Get all data
    shahid_data = get_shahid_epg()
    adtv_data = get_adtv_epg()
    alkass_data = get_alkass_epg()
    atlaspro_data = get_atlaspro_epg()
    
    # Get channel maps
    shahid_channel_map = get_shahid_channel_map()
    adtv_channel_map = get_adtv_channel_map()
    alkass_channel_map = get_alkass_channel_map()
    atlaspro_channel_map = get_atlaspro_channel_map()
    
    # Create XML root
    tv = ET.Element('tv')
    tv.set('source-info-name', 'FennecSat.com EPG')
    tv.set('source-info-url', 'https://fennecsat.com')
    tv.set('generator-info-name', 'FennecSat.com EPG')
    tv.set('generator-info-url', 'https://fennecsat.com')
    
    # Add channels
    print("Adding channels to EPG...")
    for channel_map in [shahid_channel_map, adtv_channel_map, alkass_channel_map, atlaspro_channel_map]:
        for channel_id, channel_info in channel_map.items():
            channel = ET.SubElement(tv, 'channel')
            channel.set('id', channel_info['tvg_id'])
            display_name = ET.SubElement(channel, 'display-name')
            display_name.text = channel_info['name']
    
    # Add programmes
    print("Adding Shahid programmes...")
    add_shahid_programmes(tv, shahid_data, shahid_channel_map)
    
    print("Adding ADTV programmes...")
    add_adtv_programmes(tv, adtv_data, adtv_channel_map)
    
    print("Adding AlKass programmes...")
    add_alkass_programmes(tv, alkass_data, alkass_channel_map)
    
    print("Adding AtlasPro programmes...")
    add_atlaspro_programmes(tv, atlaspro_data, atlaspro_channel_map)
    
    # Write to file
    print("Writing EPG to file...")
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        f.write('<?xml version="1.0" encoding="UTF-8"?>\n')
        f.write('<!DOCTYPE tv SYSTEM "xmltv.dtd">\n')
        f.write('<!-- Generated with FennecSat.com EPG -->\n')
        f.write(prettify(tv))
    
    print(f"EPG generated successfully at {OUTPUT_FILE}")

def add_shahid_programmes(tv, data, channel_map):
    """Add Shahid programmes to XML."""
    if 'items' not in data:
        return
        
    for channel_data in data['items']:
        channel_id = channel_data.get('channelId')
        if channel_id not in channel_map:
            continue
            
        tvg_id = channel_map[channel_id]['tvg_id']
        
        for program in channel_data.get('items', []):
            if program.get('emptySlot'):
                continue
                
            try:
                start = datetime.strptime(program['from'], '%Y-%m-%dT%H:%M:%S.%fZ')
                stop = datetime.strptime(program['to'], '%Y-%m-%dT%H:%M:%S.%fZ')
                
                programme = ET.SubElement(tv, 'programme')
                programme.set('start', start.strftime('%Y%m%d%H%M%S %z'))
                programme.set('stop', stop.strftime('%Y%m%d%H%M%S %z'))
                programme.set('channel', tvg_id)
                
                title = ET.SubElement(programme, 'title')
                title.text = program.get('title', '')
                
                if program.get('description'):
                    desc = ET.SubElement(programme, 'desc')
                    desc.text = program.get('description')
            except:
                continue

def add_adtv_programmes(tv, data, channel_map):
    """Add ADTV programmes to XML."""
    if 'response' not in data:
        return
        
    for channel_data in data['response']:
        channel_id = channel_data.get('channelExternalId')
        if channel_id not in channel_map:
            continue
            
        tvg_id = channel_map[channel_id]['tvg_id']
        
        for program in channel_data.get('programs', []):
            try:
                start = datetime.fromtimestamp(program['startDate'] / 1000)
                stop = datetime.fromtimestamp(program['endDate'] / 1000)
                
                programme = ET.SubElement(tv, 'programme')
                programme.set('start', start.strftime('%Y%m%d%H%M%S %z'))
                programme.set('stop', stop.strftime('%Y%m%d%H%M%S %z'))
                programme.set('channel', tvg_id)
                
                title = ET.SubElement(programme, 'title')
                title.text = program.get('name', '')
                
                if program.get('description'):
                    desc = ET.SubElement(programme, 'desc')
                    desc.text = program.get('description')
            except:
                continue

def add_alkass_programmes(tv, data, channel_map):
    """Add AlKass programmes to XML."""
    for channel_id, programmes in data.items():
        if channel_id not in channel_map:
            continue
            
        tvg_id = channel_map[channel_id]['tvg_id']
        qatar_tz = pytz.timezone('Asia/Qatar')
        
        for i in range(len(programmes)):
            program = programmes[i]
            next_program = programmes[i + 1] if i + 1 < len(programmes) else None
            
            try:
                start = datetime.strptime(program['start'], '%Y-%m-%d %H:%M:%S')
                start = qatar_tz.localize(start)
                
                if next_program:
                    stop = datetime.strptime(next_program['start'], '%Y-%m-%d %H:%M:%S')
                    stop = qatar_tz.localize(stop)
                else:
                    stop = start + timedelta(hours=1)
                
                programme = ET.SubElement(tv, 'programme')
                programme.set('start', start.strftime('%Y%m%d%H%M%S %z'))
                programme.set('stop', stop.strftime('%Y%m%d%H%M%S %z'))
                programme.set('channel', tvg_id)
                
                title = ET.SubElement(programme, 'title')
                title.text = program.get('title', '')
            except:
                continue

def add_atlaspro_programmes(tv, data, channel_map):
    """Add AtlasPro programmes to XML."""
    for programme in data:
        channel_id = programme['channel_id']
        if channel_id not in channel_map:
            continue
            
        channel_info = channel_map[channel_id]
        tvg_id = channel_info['tvg_id']
        
        try:
            programme_elem = ET.SubElement(tv, 'programme')
            programme_elem.set('start', programme['start'])
            programme_elem.set('stop', programme['stop'])
            programme_elem.set('channel', tvg_id)
            
            title = ET.SubElement(programme_elem, 'title')
            title.text = programme['title']
            
            if programme['desc']:
                desc = ET.SubElement(programme_elem, 'desc')
                desc.text = programme['desc']
                
            if 'icon' in channel_info and channel_info['icon']:
                icon = ET.SubElement(programme_elem, 'icon')
                icon.set('src', channel_info['icon'])
        except:
            continue

if __name__ == "__main__":
    generate_epg()
