# Builds the audience pages and guides from the data below.
# Run from the repo root: python3 tools/build.py   (PREVIEW=1 adds noindex)
import html, json, os, urllib.parse

PREVIEW = os.environ.get('PREVIEW', '1') == '1'
SITE = 'https://catchframemedia.com'
WA = '972528777496'

def e(s): return html.escape(s, quote=True)

HEAD = '''<!doctype html>
<html lang="he" dir="rtl">
<head>
<!-- Google tag -->
<script async src="https://www.googletagmanager.com/gtm.js?id=GTM-MCX7GZDL"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){{dataLayer.push(arguments);}}
  gtag('js', new Date());
</script>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
{robots}<title>{title}</title>
<link rel="canonical" href="{url}">
<meta name="description" content="{desc}">
<meta property="og:type" content="{ogtype}">
<meta property="og:locale" content="he_IL">
<meta property="og:site_name" content="CatchFrame Media">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{SITE}/img/og.jpg">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#000000">
<link rel="icon" type="image/png" sizes="32x32" href="/img/favicon-32.png">
<link rel="apple-touch-icon" href="/img/apple-touch-icon.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Rubik:wght@400;500;600;700;800&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/css/site.css">
{schema}
</head>
<body>
<header>
<nav class="nav" aria-label="ניווט ראשי">
<a href="/" aria-label="CatchFrame Media, לדף הבית"><img src="/img/logo.png" alt="CatchFrame Media" width="114" height="60"></a>
<div class="nav-links">
<a href="/schools/">בתי ספר</a>
<a href="/nonprofits/">עמותות</a>
<a href="/bar-bat-mitzvah/">בר ובת מצווה</a>
<a href="/business/">עסקים</a>
<a href="/guides/">מדריכים</a>
<a href="https://wa.me/{WA}" class="btn btn-dark" target="_blank" rel="noopener">בואו נדבר</a>
</div>
</nav>
</header>
<main>
'''

FOOT = '''</main>
<footer>
<div class="wrap">
<a href="/" class="logo-chip"><img src="/img/logo.png" alt="CatchFrame Media" width="84" height="44"></a>
<span><a href="/schools/" style="color:inherit">בתי ספר</a> · <a href="/nonprofits/" style="color:inherit">עמותות</a> · <a href="/bar-bat-mitzvah/" style="color:inherit">בר ובת מצווה</a> · <a href="/business/" style="color:inherit">עסקים</a> · <a href="/guides/" style="color:inherit">מדריכים</a></span>
<span dir="ltr">© 2026 CatchFrame Media</span>
</div>
</footer>
<script>
document.querySelectorAll('.lite').forEach(function(b){b.addEventListener('click',function(){
var f=document.createElement('iframe');f.src='https://www.youtube-nocookie.com/embed/'+b.dataset.v+'?autoplay=1&rel=0&modestbranding=1';
f.title=b.getAttribute('aria-label');f.allow='autoplay; encrypted-media; picture-in-picture; fullscreen';f.allowFullscreen=true;b.innerHTML='';b.appendChild(f);
if(window.gtag)gtag('event','video_play',{video_id:b.dataset.v});});});
document.addEventListener('click',function(e){var a=e.target.closest('a');if(!a||!window.gtag)return;var h=a.getAttribute('href')||'';
if(h.indexOf('wa.me')>-1)gtag('event','generate_lead',{method:'whatsapp'});
else if(h.indexOf('mailto:')===0)gtag('event','generate_lead',{method:'email'});
else if(h.indexOf('tel:')===0)gtag('event','generate_lead',{method:'phone'});});
</script>
</body>
</html>
'''

def wa(text): return f'https://wa.me/{WA}?text=' + urllib.parse.quote(text)

def crumbs(items):
    parts = ['<a href="/">דף הבית</a>'] + [f'<a href="{u}">{e(n)}</a>' if u else e(n) for n, u in items]
    return '<nav class="crumbs wrap" aria-label="פירורי לחם">' + ' / '.join(parts) + '</nav>'

def videos(vs):
    out = []
    for vid, name in vs:
        out.append(f'<div><button type="button" class="lite" data-v="{vid}" aria-label="צפייה: {e(name)}"><img src="https://i.ytimg.com/vi/{vid}/hqdefault.jpg" alt="" loading="lazy"><span class="play"><span><svg width="20" height="20" viewBox="0 0 16 16" fill="#F7F5F0" aria-hidden="true"><path d="M4.5 2.5l9 5.5-9 5.5z"/></svg></span></span></button><p class="vcap">{e(name)}</p></div>')
    return '<div class="vgrid">' + ''.join(out) + '</div>'

def faq_html(faq):
    return ''.join(f'<details><summary>{e(q)}</summary><p>{e(a)}</p></details>' for q, a in faq)

def schema(objs):
    return '\n'.join('<script type="application/ld+json">\n' + json.dumps(o, ensure_ascii=False) + '\n</script>' for o in objs)

def write(path, title, desc, body, objs, ogtype='website'):
    url = SITE + path
    page = HEAD.format(robots='<meta name="robots" content="noindex,nofollow">\n' if PREVIEW else '',
                       title=e(title), url=url, desc=e(desc), ogtype=ogtype, schema=schema(objs), SITE=SITE, WA=WA) + body + FOOT
    d = '.' + path
    os.makedirs(d, exist_ok=True)
    open(d + 'index.html', 'w', encoding='utf-8').write(page)

def bc(items):
    lst = [{"@type": "ListItem", "position": 1, "name": "דף הבית", "item": SITE + '/'}]
    for i, (n, u) in enumerate(items, 2):
        lst.append({"@type": "ListItem", "position": i, "name": n, "item": SITE + u})
    return {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": lst}

PROCESS = [
    ('שיחת היכרות', 'מדברים בטלפון או בוואטסאפ: מה המטרה, למי מדברים ואיפה הסרטון יוצג.'),
    ('תסריט וסטוריבורד', 'תסריט וסטוריבורד שמראה איך כל סצנה תיראה. אתם מאשרים, ורק אז מפיקים.'),
    ('הפקה ב-AI', 'דמויות, עולמות, קריינות ומוזיקה, בסגנון שבחרנו יחד.'),
    ('תיקונים ומסירה', 'סבב תיקונים, וקבצים מוכנים לכל מסך.'),
]

def process_html():
    lis = ''.join(f'<li><span class="num">0{i}</span><h3>{e(t)}</h3><p>{e(d)}</p></li>' for i, (t, d) in enumerate(PROCESS, 1))
    return f'<section class="sec dark"><div class="wrap stack" style="gap:52px"><h2 class="h2">איך זה עובד</h2><ol class="steps">{lis}</ol></div></section>'

def cta(text, msg):
    return f'''<section class="sec black"><div class="wrap stack" style="gap:20px;max-width:900px">
<h2 class="h2">{e(text)}</h2>
<p style="color:var(--muted);font-size:20px">כמה מילים על מה שאתם צריכים, ונחזור אליכם.</p>
<div class="btn-row"><a href="{wa(msg)}" class="btn btn-gold" target="_blank" rel="noopener">שלחו הודעה בוואטסאפ</a><a href="tel:+{WA}" class="btn btn-ghost" dir="ltr">052-8777496</a></div>
</div></section>'''

# ---------- audience pages ----------
AUD = [
 dict(path='/schools/', short='בתי ספר',
  title='סרטוני AI לבתי ספר | CatchFrame Media',
  desc='סרטוני AI לבתי ספר: סרטון תדמית, פתיחת שנה, טקסים, ימי זיכרון ויובל לבית הספר. תסריט, הפקה ומסירה, עם אישור שלכם בכל שלב.',
  h1='סרטוני AI לבתי ספר',
  lead='סרטון שמראה מה מיוחד בבית הספר שלכם, ומדבר לתלמידים, להורים ולצוות.',
  intro=['במקום עוד מצגת בטקס, סרטון עם דמויות, עולם וסיפור שנכתבו במיוחד בשבילכם. אפשר לבנות את הדמויות לפי תמונות של התלמידים, המורים או המבנה, כך שכולם יזהו את עצמם על המסך.',
         'עבדנו עם בתי ספר על סרטוני תדמית, פתיחת שנה, חגיגת יובל וסרטונים שמלווים את הקהילה בתקופות קשות. כל סרטון מתחיל בשיחה עם ההנהלה: מה רוצים להגיד, למי, ואיפה הוא יוצג.'],
  uses=['סרטון תדמית לבית הספר', 'פתיחת שנת לימודים', 'טקסים וימי זיכרון', 'יובל וחגיגות לבית הספר', 'הסברה וערכים', 'סיום שנה ופרידה משכבה'],
  vids=[('M6XtYe8n5j0','בית ספר ניל"י, זכרון יעקב: 140 שנה'),('llEfuPIRctU','בית ספר כנפי אבירים, יבנה'),('l0lTXNQeg3Q','בית ספר צליל, חדרה'),('7EdqKVEpfCI','בית ספר ניל"י: פתיחת שנת הלימודים'),('QvQw0ShNmw4','בית ספר ירושלים, קריית אתא: איך מקבלים מורה חדשה?')],
  faq=[('כמה זמן מראש צריך להזמין לפני טקס?','מומלץ לפנות כמה שבועות לפני. כך יש זמן לתסריט, לאישורים ולסבב תיקונים בלי לחץ.'),
       ('אפשר להשתמש בתמונות של תלמידים?','כן, באישור בית הספר. התמונות עוזרות לבנות דמויות שדומות למציאות, ואפשר גם לעבוד בלי תמונות של ילדים בכלל.'),
       ('מי מאשר את התוכן?','אתם. התסריט והסטוריבורד עוברים אישור לפני שמתחילים להפיק, ויש סבב תיקונים על הסרטון עצמו.')],
  cta='יש לכם טקס או אירוע בקרוב?', msg='היי נירית, אשמח לשמוע על סרטון AI לבית הספר שלנו'),
 dict(path='/nonprofits/', short='עמותות',
  title='סרטוני AI לעמותות ולארגונים | CatchFrame Media',
  desc='סרטוני AI לעמותות: הסברה, גיוס תרומות, העלאת מודעות וסיפורי השפעה. מספרים את העשייה שלכם בשפה שהקהל מתחבר אליה.',
  h1='סרטוני AI לעמותות',
  lead='העשייה שלכם, בסרטון שאנשים צופים בו עד הסוף ומשתפים.',
  intro=['לעמותות יש סיפורים חזקים, אבל לא תמיד אפשר לצלם אותם: אנשים שלא רוצים להיחשף, תהליכים שלוקחים שנים, או רעיון שקשה להסביר במילים. בסרטון AI אפשר להראות את כל זה בלי מצלמה.',
         'נבנה יחד את המסר, נכתוב תסריט שמתאים לקהל שלכם, תורמים, מתנדבים או הציבור הרחב, ונפיק סרטון שמתאים לאירוע, לאתר ולרשתות.'],
  uses=['גיוס תרומות', 'העלאת מודעות', 'הצגת תוכנית או פרויקט', 'סיפורי השפעה', 'ימי מודעות וקמפיינים', 'אירועי הוקרה למתנדבים'],
  vids=[('s1ic4NTYNHw','עמותת חממה: חיבורים להצלחה'),('5YY-4TvfIho','"ללכת על ביצים": יום המאבק באלימות נגד נשים'),('a2hfco_y4vE','פרויקט סאנשיין')],
  faq=[('אפשר לספר סיפור של אנשים בלי לחשוף אותם?','כן. דמויות AI מאפשרות לספר סיפור אמיתי בלי להראות פנים אמיתיות.'),
       ('הסרטון מתאים גם לרשתות?','כן. אפשר לקבל גרסה ארוכה לאירוע ולאתר, וגרסאות קצרות לרילס, טיקטוק ויוטיוב.'),
       ('כמה זה עולה?','תלוי באורך, בסגנון ובמורכבות. ספרו לנו על הפרויקט ותקבלו הצעת מחיר מפורטת.')],
  cta='רוצים לספר את הסיפור של הארגון?', msg='היי נירית, אשמח לשמוע על סרטון AI לעמותה שלנו'),
 dict(path='/bar-bat-mitzvah/', short='בר ובת מצווה',
  title='סרטון AI לבר מצווה ובת מצווה | CatchFrame Media',
  desc='סרטון AI אישי לבר מצווה ולבת מצווה: הסיפור של הילד או הילדה, עם דמויות שנבנות לפי התמונות שלכם. במקום עוד מצגת תמונות.',
  h1='סרטון AI לבר ובת מצווה',
  lead='במקום עוד מצגת תמונות: סרטון שמספר את הסיפור של הילד או הילדה, ומרגש את כל האולם.',
  intro=['שולחים לנו תמונות וקצת סיפורים, ואנחנו בונים מהם סרטון: הילד או הילדה כדמות, המשפחה, התחביבים והרגעים שחשוב לכם להראות. הכול בעולם ויזואלי שבוחרים יחד, מאגדה ועד סרט גיבורים.',
         'אפשר גם לשלב ברכות מהמשפחה, קריינות או שיר. מקבלים קובץ מוכן להקרנה באולם, ועוד גרסה קצרה לשיתוף.'],
  uses=['סרטון פתיחה לאירוע', 'הסיפור של הילד או הילדה', 'ברכה מההורים', 'סרטון לתאומים', 'הפתעה מהאחים', 'גרסה קצרה לשיתוף'],
  vids=[('nD0N-Rh4nMY','סרטון לבר מצווה'),('glTZpROFGLE','התאומים שרף, יום הולדת 70'),('Ild9A0ipYYg','החתונה של כרמל ויגאל')],
  faq=[('כמה זמן לפני האירוע צריך להזמין?','כדאי לפנות כמה שבועות מראש, כדי שיהיה זמן לתסריט, לאישור ולסבב תיקונים.'),
       ('אילו תמונות לשלוח?','כמה תמונות ברורות של הפנים מזוויות שונות, ותמונות של רגעים שחשוב לכם להראות. ככל שהתמונות ברורות יותר, הדמויות דומות יותר.'),
       ('אפשר לשים שיר מוכר ברקע?','בסרטון להקרנה באירוע זה אפשרי. אם רוצים להעלות אותו ליוטיוב או לרשתות, עדיף מוזיקה חופשית, כי שירים מסחריים נחסמים שם.')],
  cta='יש לכם בר או בת מצווה בקרוב?', msg='היי נירית, אשמח לשמוע על סרטון AI לבר/בת מצווה'),
 dict(path='/business/', short='עסקים',
  title='סרטוני AI לעסקים: תדמית, מוצר ופרסום | CatchFrame Media',
  desc='סרטוני AI לעסקים: סרטון תדמית, סרטון מוצר ופרסומות לרשתות. מספרים מי אתם ולמה דווקא אתם, בלי צילומים ובלי הפקה כבדה.',
  h1='סרטוני AI לעסקים',
  lead='מי אתם ולמה דווקא אתם, בסרטון לאתר, לפרסום ולרשתות.',
  intro=['סרטון תדמית או פרסומת בלי יום צילום, בלי שחקנים ובלי לוקיישן. דמויות, מקומות וסצנות שבצילום רגיל היו עולים הון, נבנים ב-AI לפי התסריט.',
         'מתחילים מהמסר: מה העסק עושה, למי, ומה מבדיל אותו. משם כותבים תסריט קצר וקולע, ומפיקים גרסאות לכל פלטפורמה.'],
  uses=['סרטון תדמית', 'סרטון מוצר או שירות', 'פרסומת לרשתות', 'קמפיין לחג או לעונה', 'גיבור או דמות למותג', 'גרסאות לרילס, טיקטוק ויוטיוב'],
  vids=[('fSGAmRSNyXk','רולדין: סרטון לחנוכה'),('EAkBm2lWV_k','KM Motors, חדרה')],
  faq=[('כמה זמן לוקח להפיק סרטון לעסק?','תלוי באורך ובמורכבות. בשיחה הראשונה נקבע לוח זמנים לפי הקמפיין שלכם.'),
       ('אפשר לבנות דמות קבועה למותג?','כן. אפשר ליצור דמות שחוזרת בכל הסרטונים, כמו "בטונית" שיצרנו ל-FindU.'),
       ('מקבלים גרסאות לרשתות?','כן. אפשר לקבל גרסה ראשית וגרסאות קצרות בפורמט אנכי לרילס וטיקטוק.')],
  cta='רוצים סרטון לעסק?', msg='היי נירית, אשמח לשמוע על סרטון AI לעסק שלי'),
]

for p in AUD:
    uses = ''.join(f'<li>{e(u)}</li>' for u in p['uses'])
    intro = ''.join(f'<p>{e(x)}</p>' for x in p['intro'])
    others = ''.join(f'<a href="{q["path"]}"><strong>{e(q["h1"])}</strong><span>{e(q["lead"])}</span></a>' for q in AUD if q is not p)
    body = f'''<section class="page-hero">{crumbs([(p['short'], None)])}
<div class="wrap"><span class="tag">We catch your frame</span><h1>{e(p['h1'])}</h1><p class="lead">{e(p['lead'])}</p>
<div class="btn-row"><a href="{wa(p['msg'])}" class="btn btn-gold" target="_blank" rel="noopener">שלחו הודעה בוואטסאפ</a><a href="#work" class="btn btn-ghost">לסרטונים</a></div></div></section>
<section class="sec light"><div class="wrap"><div class="prose stack">{intro}<h2>מה אפשר לעשות</h2><ul class="list2" style="font-size:20px">{uses}</ul></div></div></section>
<section class="sec dark" id="work"><div class="wrap stack" style="gap:40px"><h2 class="h2">עבודות</h2>{videos(p['vids'])}</div></section>
{process_html()}
<section class="sec" style="background:var(--panel)"><div class="faq stack"><h2 class="h2">שאלות נפוצות</h2><div class="stack" style="gap:12px">{faq_html(p['faq'])}</div></div></section>
<section class="sec light"><div class="wrap stack" style="gap:28px"><h2 class="h2">עוד תחומים</h2><div class="cards-links">{others}</div></div></section>
{cta(p['cta'], p['msg'])}
'''
    objs = [
        {"@context": "https://schema.org", "@type": "Service", "name": p['h1'], "description": p['desc'], "areaServed": "ישראל",
         "provider": {"@type": "ProfessionalService", "name": "CatchFrame Media", "url": SITE + '/', "telephone": "+972-52-877-7496"}},
        {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in p['faq']]},
        bc([(p['short'], p['path'])]),
    ]
    write(p['path'], p['title'], p['desc'], body, objs)

# ---------- guides ----------
GUIDES = [
 dict(slug='ai-video-price', title='כמה עולה סרטון AI? מה קובע את המחיר',
  desc='ממה מורכב המחיר של סרטון AI: אורך, סגנון, מספר דמויות, קריינות ומוזיקה. ומה לבקש שיופיע בהצעת המחיר.',
  intro='"כמה זה עולה?" היא השאלה הראשונה שכולם שואלים, ובצדק. התשובה הכנה היא שזה תלוי, אבל אפשר לדעת בדיוק במה.',
  sections=[
   ('מה משפיע על המחיר', ['<b>אורך הסרטון.</b> סרטון של דקה דורש פחות סצנות, פחות תסריט ופחות עבודה מסרטון של שלוש דקות.',
                          '<b>מספר הדמויות.</b> דמות שנבנית לפי תמונה של אדם אמיתי דורשת עבודה כדי שתיראה דומה ועקבית לאורך כל הסרטון.',
                          '<b>הסגנון.</b> אנימציה פשוטה, סגנון מצויר או סרט גיבורים מלא, כל אחד דורש כמות עבודה אחרת.',
                          '<b>קריינות ומוזיקה.</b> קריינות, שיר או מוזיקה מותאמת מוסיפים שכבה להפקה.',
                          '<b>גרסאות.</b> גרסה להקרנה, גרסה קצרה לרשתות, גרסה אנכית לרילס.']),
   ('מה כדאי שיופיע בהצעת מחיר', ['מה כלול: תסריט, סטוריבורד, הפקה, קריינות, מוזיקה וכתוביות.', 'כמה סבבי תיקונים כלולים.', 'אילו קבצים מקבלים ובאילו פורמטים.', 'לוח זמנים, ומה קורה אם יש תאריך יעד.']),
   ('איך לקבל הצעה מדויקת', ['ספרו בכמה מילים מה האירוע או המטרה, מי הקהל, ובערך כמה זמן אתם רוצים שהסרטון יהיה. אם יש סרטון שאהבתם, שלחו אותו כדוגמה. ככה אפשר לתת מחיר שלא משתנה בדרך.']),
  ], rel='/schools/', relname='סרטוני AI לבתי ספר'),
 dict(slug='bar-mitzvah-video-ideas', title='רעיונות לסרטון בר מצווה ובת מצווה',
  desc='רעיונות לסרטון בר ובת מצווה שמרגש את האולם: הילד כגיבור, מסע בזמן, עולם התחביבים וברכה מהמשפחה. ואיך לבחור את הנכון לכם.',
  intro='מצגת תמונות עם שיר ברקע כולם כבר ראו. הנה כמה כיוונים לסרטון שאנשים באמת יזכרו אחרי האירוע.',
  sections=[
   ('הילד או הילדה כגיבורי הסרט', ['סרט הרפתקאות קצר שבו הילד הוא הדמות הראשית: מתמודד עם אתגר, נעזר בחברים ובמשפחה, ומגיע ליום הגדול. עובד במיוחד כסרטון פתיחה.']),
   ('מסע בזמן', ['מהלידה ועד היום, כשכל תקופה מקבלת סצנה משלה: הגן, הכיתה הראשונה, החוג, הטיול המשפחתי. אפשר לבנות את הסצנות לפי תמונות אמיתיות מכל גיל.']),
   ('העולם של התחביב', ['כדורגל, ריקוד, מוזיקה, מיינקראפט. הסרטון מתרחש בתוך העולם שהילד הכי אוהב, וכל המשפחה מופיעה שם כדמויות.']),
   ('ברכה מההורים', ['במקום נאום, ההורים מספרים את הסיפור, והסרטון מראה אותו. מרגש במיוחד, ולא צריך לעמוד מול כולם עם דף.']),
   ('לתאומים', ['שני גיבורים, סיפור אחד. אפשר להראות את מה שמשותף להם ואת מה שהופך כל אחד לייחודי.']),
   ('איך בוחרים', ['שאלו את עצמכם מה הכי מאפיין את הילד, ומה אתם רוצים שהאורחים ירגישו: צחוק, התרגשות או גאווה. משם הכיוון בדרך כלל ברור. ואם לא, בשיחה הראשונה נחשוב עליו יחד.']),
  ], rel='/bar-bat-mitzvah/', relname='סרטון AI לבר ובת מצווה'),
 dict(slug='school-memorial-day-video', title='סרטון ליום הזיכרון בבית ספר: איך עושים את זה נכון',
  desc='איך להכין סרטון ליום הזיכרון בבית ספר: תיאום עם המשפחות, בחירת הסיפור, טון ומוזיקה, ומתי להתחיל. מדריך לרכזות ולמנהלות.',
  intro='סרטון ליום הזיכרון הוא אחד הדברים הרגישים ביותר שבית ספר מכין. הנה מה שחשוב לדעת לפני שמתחילים.',
  sections=[
   ('מתחילים מהמשפחות', ['אם הסרטון מספר על חללים מהקהילה, הכול מתחיל בשיחה עם המשפחות: מה הן רוצות שיסופר, אילו תמונות אפשר להשתמש בהן, ומה לא. כדאי שהמשפחה תראה את התסריט לפני ההפקה.']),
   ('סיפור אחד, לא רשימה', ['סרטון שמנסה לספר הכול לא מספר כלום. עדיף לבחור רגע, תכונה או סיפור אחד שמייצג את האדם, ולבנות סביבו.']),
   ('טון ומוזיקה', ['פשוט ומכבד. בלי אפקטים מיותרים, בלי דרמה מלאכותית. מוזיקה שקטה, וקריינות או טקסט שנכתבו בשפה של התלמידים.']),
   ('למה דווקא AI', ['כשיש מעט תמונות, או רק תמונות ישנות, אפשר לבנות סצנות מהחיים של האדם: הבית, הכיתה, המקום שאהב. תמיד באישור המשפחה, ותמיד בעדינות.']),
   ('מתי להתחיל', ['תיאום עם משפחות, כתיבה ואישורים לוקחים זמן. כדאי להתחיל לפחות חודש לפני הטקס, ועדיף יותר.']),
  ], rel='/schools/', relname='סרטוני AI לבתי ספר'),
 dict(slug='graduation-video-school', title='סרטון סיום לכיתה ו׳ או י״ב: מה מכינים ומתי מתחילים',
  desc='איך מכינים סרטון סיום לכיתה ו׳ או י״ב: בוחרים רעיון, אוספים תמונות, קובעים מי מאשר, ומתחילים בזמן.',
  intro='סרטון הסיום הוא מה שנשאר לתלמידים ולהורים אחרי שהמסיבה נגמרת. ההכנה מתחילה הרבה לפני יוני, ומי שמתחיל בחורף רגוע באביב.',
  sections=[
   ('בוחרים רעיון אחד', ['השנים בבית הספר כמסע אחד, הכיתה כצוות גיבורים, או מכתב לעצמנו בעוד עשר שנים. עדיף כיוון אחד ברור מכמה רעיונות שנדחסים לסרטון אחד.']),
   ('אוספים תמונות מוקדם', ['תמונות של התלמידים עוזרות לדמויות להיראות כמו הילדים האמיתיים. בקשו מההורים תמונות כבר עכשיו, ובדקו שכל ילד וילדה מופיעים.']),
   ('קובעים מי מאשר', ['מחנכת, רכזת, נציג ועד: החליטו מראש מי מאשר את התסריט. ככה הוא מאושר פעם אחת ולא עובר עשר ידיים.']),
   ('איך זה עובד מול ההפקה', ['שיחת היכרות, תסריט וסטוריבורד שאתם מאשרים, ורק אז הפקה. אחרי ההפקה יש סבב תיקונים, ומקבלים קבצים להקרנה באולם ולשליחה להורים.']),
   ('מתי מתחילים', ['מסיבות הסיום מתרכזות בסוף השנה, וכולם רוצים את אותם שבועות. כדאי לסגור רעיון ותקציב כבר בחורף, ולהשאיר זמן לאישורים.']),
   ('כמה זה עולה', ['תלוי באורך, בסגנון ובמורכבות. פירטנו את זה במדריך <a href="/guides/ai-video-price/">כמה עולה סרטון AI</a>.']),
  ], rel='/schools/', relname='סרטוני AI לבתי ספר'),
]

cards = []
for g in GUIDES:
    path = f'/guides/{g["slug"]}/'
    secs = ''
    for h, ps in g['sections']:
        secs += f'<h2>{e(h)}</h2>'
        if len(ps) > 1:
            secs += '<ul>' + ''.join(f'<li>{x}</li>' for x in ps) + '</ul>'
        else:
            secs += f'<p>{ps[0]}</p>'
    body = f'''<section class="page-hero">{crumbs([('מדריכים', '/guides/'), (g['title'], None)])}
<div class="wrap"><span class="tag">מדריך</span><h1>{e(g['title'])}</h1><p class="lead">{e(g['intro'])}</p></div></section>
<section class="sec light"><div class="wrap"><article class="prose stack">{secs}
<p style="margin-top:20px">רוצים לראות דוגמאות? <a href="{g['rel']}">{e(g['relname'])}</a></p>
<p style="color:#6B6760;font-size:17px">נכתב על ידי נירית אלקובי, יוצרת וידאו ותסריטאית, CatchFrame Media.</p></article></div></section>
{cta('יש לכם שאלה? כתבו לנו.', 'היי נירית, קראתי את המדריך "' + g['title'] + '" ויש לי שאלה')}
'''
    objs = [{"@context": "https://schema.org", "@type": "Article", "headline": g['title'], "description": g['desc'], "inLanguage": "he",
             "author": {"@type": "Person", "name": "נירית אלקובי"}, "publisher": {"@type": "Organization", "name": "CatchFrame Media", "logo": {"@type": "ImageObject", "url": SITE + '/img/logo.png'}},
             "datePublished": "2026-11-21", "mainEntityOfPage": SITE + path, "image": SITE + '/img/og.jpg'},
            bc([('מדריכים', '/guides/'), (g['title'], path)])]
    write(path, g['title'] + ' | CatchFrame Media', g['desc'], body, objs, ogtype='article')
    cards.append(f'<a href="{path}"><strong>{e(g["title"])}</strong><span>{e(g["desc"])}</span></a>')

body = f'''<section class="page-hero">{crumbs([('מדריכים', None)])}
<div class="wrap"><span class="tag">מדריכים</span><h1>מדריכים וטיפים לסרטוני AI</h1><p class="lead">תשובות לשאלות שהכי שואלים אותנו: מחירים, רעיונות, ואיך מתכוננים לסרטון.</p></div></section>
<section class="sec light"><div class="wrap"><div class="cards-links">{''.join(cards)}</div></div></section>
{cta('לא מצאתם תשובה? כתבו לנו.', 'היי נירית, יש לי שאלה על סרטון AI')}
'''
write('/guides/', 'מדריכים וטיפים לסרטוני AI | CatchFrame Media', 'מדריכים לסרטוני AI: כמה זה עולה, רעיונות לבר ובת מצווה, סרטון ליום הזיכרון וסרטון סיום שנה בבית ספר.', body, [bc([('מדריכים', '/guides/')])])
print('built', len(AUD), 'audience pages and', len(GUIDES), 'guides; preview =', PREVIEW)
