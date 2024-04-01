from enum import Enum


class Browser(Enum):
    Chrome = (
        "https://chromewebstore.google.com/detail/tampermonkey/dhdgffkkebhmkfjojejmpbldmpobfkfo"
    )
    Edge = "https://microsoftedge.microsoft.com/addons/detail/iikmkjmpaadaobahmlepeloendndfphd"
    Firefox = "https://addons.mozilla.org/en-US/firefox/addon/tampermonkey/"
    Safari = "https://apps.apple.com/us/app/tampermonkey/id1482490089"
    Opera = "https://addons.opera.com/en/extensions/details/tampermonkey-beta/"
    Unknown = "https://www.tampermonkey.net/index.php?"
