import urllib.parse as up

items = [
    "'Blueberries' Buckshot | NSWC SEAL",
    "'The Doctor' Romanov | Sabre",
    "'Two Times' McCoy | TACP Cavalry",
    "'Two Times' McCoy | USAF TACP",
    "2020 RMR Challengers",
    "AK-47 | Aquamarine Revenge (Field-Tested)",
    "AK-47 | Asiimov (Field-Tested)",
    "AK-47 | Frontside Misty (Minimal Wear)",
    "AK-47 | Legion of Anubis (Factory New)",
    "AK-47 | Neon Revolution (Minimal Wear)",
    "AK-47 | Neon Rider (Field-Tested)",
    "AK-47 | Point Disarray (Factory New)",
    "AK-47 | Safari Mesh (Field-Tested)",
    "AK-47 | Safety Net (Factory New)",
    "AK-47 | Uncharted (Minimal Wear)",
    "AK-47 | Uncharted (Well-Worn)",
    "AUG | Aristocrat (Field-Tested)",
    "AUG | Random Access (Field-Tested)",
    "AUG | Storm (Factory New)",
    "AUG | Surveillance (Field-Tested)",
    "AWP | Capillary (Minimal Wear)",
    "AWP | Pit Viper (Minimal Wear)",
    "AWP | Safari Mesh (Battle-Scarred)",
    "Arno The Overgrown | Guerrilla Warfare",
    "Aspirant | Gendarmerie Nationale",
    "B Squadron Officer | SAS",
    "Berlin 2019 Legends (Holo-Foil)",
    "Blackwolf | Sabre",
    "Bloody Darryl The Strapped | The Professionals",
    "Buckshot | NSWC SEAL",
    "CZ75-Auto | Crimson Web (Field-Tested)",
    "CZ75-Auto | Eco (Field-Tested)",
    "CZ75-Auto | Tacticat (Minimal Wear)",
    "Canals Pin",
    "Chef d'Escadron Rouchard | Gendarmerie Nationale",
    "Cmdr. Mae 'Dead Cold' Jamison | SWAT",
    "Community Sticker Capsule 1",
    "Crasswater The Forgotten | Guerrilla Warfare",
    "Desert Eagle | Blue Ply (Minimal Wear)",
    "Desert Eagle | Bronze Deco (Factory New)",
    "Desert Eagle | Corinthian (Factory New)",
    "Desert Eagle | Printstream (Minimal Wear)",
    "Desert Eagle | Light Rail (Field-Tested)",
    "Desert Eagle | Meteorite (Factory New)",
    "Desert Eagle | Oxide Blaze (Factory New)"
]

items_links = []
def convert_title_to_link(title: str) -> str:
    encoded_title = up.quote_plus(title.replace(' ', '%20'), safe='%20')
    link = 'https://steamcommunity.com/market/listings/730/' + encoded_title
    return link

for item in items: 
    items_links.append(convert_title_to_link(title=item))

proxies = []
for i in range(19300, 19999):
    proxy_data = {
        'user' : 'Lolobroller_17712',
        'pass' : 'yc44zbOJP8',
        'host' : 'ipv4.reproxy.network',
        'port' : i
    }
    proxies.append(proxy_data)