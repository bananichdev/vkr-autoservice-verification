"""Исходник рисунков ЛР3. Запуск: python3 assets/design/generate_diagrams.py.

Используется только стандартная библиотека. SVG содержат обычные фигуры и текст,
поэтому их также можно открыть и отредактировать в векторном редакторе.
"""

from html import escape
from pathlib import Path


INK = "#26364a"
BLUE = "#eaf2fc"
GREEN = "#e9f5ef"
GREY = "#f1f3f6"
AMBER = "#fff5df"


class Figure:
    def __init__(self, width, height, title, subtitle):
        self.width, self.height = width, height
        self.parts = [
            f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
            f'viewBox="0 0 {width} {height}" role="img" aria-labelledby="title desc">',
            f'<title id="title">{escape(title)}</title><desc id="desc">{escape(subtitle)}</desc>',
            '<defs><marker id="arrow" markerWidth="10" markerHeight="10" refX="8" refY="5" '
            'orient="auto-start-reverse" markerUnits="userSpaceOnUse">'
            f'<path d="M 1 1 L 8 5 L 1 9" fill="none" stroke="{INK}" stroke-width="2"/>'
            '</marker></defs>',
            '<rect width="100%" height="100%" fill="white"/>',
            '<g font-family="Arial, sans-serif" fill="#26364a">',
        ]
        self.text(44, 48, title, 29, "start", True)
        self.text(44, 84, subtitle, 21, "start")

    def text(self, x, y, lines, size=22, anchor="middle", bold=False):
        if isinstance(lines, str):
            lines = lines.split("\n")
        weight = ' font-weight="700"' if bold else ""
        self.parts.append(f'<text x="{x}" y="{y}" font-size="{size}" text-anchor="{anchor}"{weight}>')
        for i, line in enumerate(lines):
            self.parts.append(f'<tspan x="{x}" dy="{0 if i == 0 else size * 1.3}">{escape(line)}</tspan>')
        self.parts.append('</text>')

    def rect(self, x, y, w, h, fill="white", radius=0, dash=False, stroke=INK):
        self.parts.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{radius}" '
                          f'fill="{fill}" stroke="{stroke}" stroke-width="2"'
                          + (' stroke-dasharray="8 6"' if dash else '') + '/>')

    def box(self, x, y, w, h, lines, fill=BLUE, size=22, radius=18):
        self.rect(x, y, w, h, fill, radius)
        if isinstance(lines, str):
            lines = lines.split("\n")
        self.text(x + w / 2, y + h / 2 - (len(lines) - 1) * size * .65 + size * .34, lines, size)

    def edge(self, points, label=None, label_pos=None, arrow=True, dash=False):
        coords = " ".join(f"{x},{y}" for x, y in points)
        self.parts.append(f'<polyline points="{coords}" fill="none" stroke="{INK}" stroke-width="2.2" '
                          + ('stroke-dasharray="7 5" ' if dash else '')
                          + ('marker-end="url(#arrow)"' if arrow else '') + '/>')
        if label:
            x, y = label_pos
            self.text(x, y, label, 20)

    def diamond(self, x, y, w=180, h=90, lines=None):
        self.parts.append(f'<polygon points="{x},{y-h/2} {x+w/2},{y} {x},{y+h/2} {x-w/2},{y}" '
                          f'fill="{AMBER}" stroke="{INK}" stroke-width="2"/>')
        if lines:
            if isinstance(lines, str):
                lines = lines.split("\n")
            self.text(x, y - (len(lines)-1)*12 + 7, lines, 20)

    def circle(self, x, y, final=False):
        if final:
            self.parts.append(f'<circle cx="{x}" cy="{y}" r="17" fill="white" stroke="{INK}" stroke-width="2"/>')
        self.parts.append(f'<circle cx="{x}" cy="{y}" r="{10 if final else 12}" fill="{INK}"/>')

    def lanes(self, titles, boundaries, bottom):
        for i, name in enumerate(titles):
            left, right = boundaries[i:i+2]
            self.rect(left, 112, right-left, bottom-112, "none", stroke="#bac4d1")
            self.rect(left, 112, right-left, 50, GREY, stroke="#bac4d1")
            self.text((left+right)/2, 145, name, 22, bold=True)

    def note(self, x, y, w, h, lines, size=21):
        self.box(x, y, w, h, lines, AMBER, size, 4)

    def save(self, name):
        Path(__file__).with_name(name).write_text("\n".join(self.parts + ['</g></svg>']) + "\n", encoding="utf-8")


def as_is():
    f = Figure(1440, 1530, "AS-IS · выбор автосервиса без аналитического модуля", "UML activity · базовая проверка реквизитов в проекте уже предусмотрена")
    f.lanes(["Автовладелец", "Почини.Онлайн", "Внешние источники"], [40, 490, 950, 1400], 1480)
    f.circle(265, 202)
    f.box(100, 250, 330, 90, "Открыть карточку\nавтосервиса")
    f.box(550, 390, 340, 110, "Показать профиль, отзывы\nи существующий статус\nпроверки реквизитов")
    f.box(100, 550, 330, 100, "Самостоятельно найти\nреквизиты исполнителя")
    f.box(1010, 700, 330, 110, "Ответить на отдельные\nзапросы к реестрам\nи судебным сведениям", GREY)
    f.box(100, 850, 330, 110, "Сопоставить сведения\nоб организации, судах\nи обращениях клиентов")
    f.diamond(265, 1040, 260, 100, "Сведения\nпонятны?")
    f.box(70, 1150, 290, 70, "Принять решение", GREEN)
    f.box(100, 1310, 330, 90, "Отложить выбор\nи продолжить поиск", AMBER)
    f.circle(215, 1250, True)
    f.circle(265, 1440, True)
    f.edge([(265, 214), (265, 250)])
    f.edge([(265, 340), (265, 445), (550, 445)])
    f.edge([(550, 470), (470, 470), (470, 600), (430, 600)])
    f.edge([(265, 650), (265, 735), (1010, 735)])
    f.edge([(1010, 785), (470, 785), (470, 905), (430, 905)])
    f.edge([(265, 960), (265, 990)])
    f.edge([(265, 1090), (265, 1150)], "[да]", (310, 1125))
    f.edge([(395, 1040), (470, 1040), (470, 1355), (430, 1355)], "[нет]", (445, 1025))
    f.edge([(215, 1220), (215, 1233)])
    f.edge([(265, 1400), (265, 1423)])
    f.note(560, 865, 340, 105, "Нет единого объяснения\nи истории проверки;\nсопоставление делает клиент")
    f.save("01-as-is.svg")


def to_be():
    f = Figure(1520, 2010, "TO-BE · единая проверка и объяснение результата", "UML activity · клиентский сценарий; очередь и ручное решение выполняются асинхронно")
    f.lanes(["Автовладелец", "Модуль проверки", "Оператор"], [40, 480, 1150, 1480], 1960)
    f.circle(240, 205)
    f.box(80, 250, 320, 90, "Открыть карточку\nвыбранного сервиса")
    f.box(670, 350, 360, 90, "Проверить текущую связь,\nверсию входов и срок данных")
    f.diamond(850, 510, 260, 110, "Карточка\nактуальна?")
    f.diamond(850, 610, 24, 24)
    f.box(670, 660, 360, 100, "Создать / найти задание;\nзафиксировать версии\nи номер проверки")
    f.box(670, 800, 360, 100, "Получить сведения реестра;\nсопоставить ЮЛ/ИП\nс конкретной точкой")
    f.diamond(850, 970, 220, 100, "Связь\nсубъекта?")
    f.box(490, 1090, 165, 135, "Зафиксировать\nпричину:\nнет данных /\nнесовпадение", AMBER, 19)
    f.box(1170, 920, 280, 110, "Проверить основания\nспорной связи;\nзапросить исправление", AMBER, 20)
    f.box(1170, 1110, 280, 110, "Зафиксировать решение;\nновая версия входов\nи новая проверка", AMBER, 20)
    f.box(670, 1120, 360, 100, "Собрать суды, жалобы\nи другие доступные факты;\nсохранить пробелы в данных")
    f.box(670, 1280, 360, 110, "Объединить дубли событий;\nоценить факторы по методике;\nподготовить объяснение", GREEN)
    f.diamond(850, 1460, 32, 32)
    f.diamond(850, 1560, 300, 130, "Версии и номер\nещё актуальны?")
    f.box(490, 1510, 165, 100, "В историю;\nтекущую\nкарточку\nне менять", AMBER, 20)
    f.circle(572, 1685, True)
    f.box(670, 1670, 360, 100, "Атомарно опубликовать\nрезультат или статус\nнедостатка сведений", GREEN)
    f.diamond(240, 1810, 32, 32)
    f.box(80, 1855, 320, 70, "Прочитать основания и даты", GREEN, 21)
    f.circle(240, 1945, True)
    f.edge([(240, 217), (240, 250)])
    f.edge([(400, 295), (520, 295), (520, 395), (670, 395)])
    f.edge([(850, 440), (850, 455)])
    f.edge([(720, 510), (60, 510), (60, 1810), (224, 1810)], "[да]", (400, 490))
    f.edge([(850, 565), (850, 598)], "[нет]", (895, 588))
    f.edge([(850, 622), (850, 660)])
    f.edge([(850, 760), (850, 800)])
    f.edge([(850, 900), (850, 920)])
    f.edge([(740, 970), (572, 970), (572, 1090)], "[нет данных / несовпадение]", (540, 1040))
    f.edge([(960, 970), (1170, 970)], "[спорная связь]", (1060, 946))
    f.edge([(850, 1020), (850, 1120)], "[подтверждена]", (940, 1072))
    f.edge([(1310, 1030), (1310, 1110)])
    f.edge([(1450, 1165), (1465, 1165), (1465, 610), (862, 610)], "новая проверка", (1270, 588))
    f.edge([(850, 1220), (850, 1280)])
    f.edge([(850, 1390), (850, 1444)])
    f.edge([(572, 1225), (572, 1460), (834, 1460)])
    f.edge([(850, 1476), (850, 1495)])
    f.edge([(700, 1560), (655, 1560)], "[нет]", (678, 1539))
    f.edge([(572, 1610), (572, 1668)])
    f.edge([(850, 1625), (850, 1670)], "[да]", (895, 1652))
    f.edge([(670, 1720), (470, 1720), (470, 1770), (240, 1770), (240, 1794)])
    f.edge([(240, 1826), (240, 1855)])
    f.edge([(240, 1925), (240, 1928)])
    f.note(1170, 1750, 280, 175, "Карточка показывает\nожидание решения.\nНет ответа источника —\nне доказательство\nотсутствия риска.", 20)
    f.save("02-to-be.svg")


def er_model():
    f = Figure(1570, 1770, "ER · данные проверки и история оснований", "Логическая модель расширения · PK — ключ, FK — ссылка; 0..N — любое число, включая ноль")
    boxes = {}
    def entity(key, x, y, title, fields):
        w, h = 420, 238
        boxes[key] = (x, y, w, h)
        f.rect(x, y, w, h, "white", 4)
        f.rect(x, y, w, 49, BLUE, 4)
        f.text(x+18, y+33, title, 23, "start", True)
        f.text(x+18, y+81, fields, 21, "start")
    entity("point", 50, 140, "Точка · ServicePoint", ["PK point_id", "name, address", "input_revision, generation", "current_binding_id?", "current_assessment_id?"])
    entity("binding", 575, 140, "Связь · SubjectBinding", ["PK binding_id; FK point_id", "FK subject_id; revision", "valid_from, valid_to?", "state, basis_ref", "0..1 подтверждённых текущих"])
    entity("subject", 1100, 140, "Субъект · LegalSubject", ["PK subject_id; kind: ЮЛ / ИП", "inn, ogrn_or_ogrnip", "registered_on, registry_status", "UNIQUE(kind, inn, ogrn_or_ogrnip)", "Возраст регистрации ≠ стаж точки"])
    entity("run", 50, 550, "Проверка · CheckRun", ["PK run_id; FK binding_id", "request_key, generation", "captured_versions, lease_epoch", "state, lease_until", "method_snapshot, input_snapshot"])
    entity("source", 575, 550, "Источник · SourceResult", ["PK source_result_id; FK run_id", "source_code, query_scope", "observed_at, source_as_of?", "outcome, coverage, valid_until", "Нормализованный снимок + хеш"])
    entity("fact", 1100, 550, "Факт · Fact", ["PK (fact_id, revision)", "FK subject_id; point_id?", "event_key, kind, event_date", "role, outcome, confirmation", "resolution, scope: ЮЛ / точка"])
    entity("audit", 50, 970, "Решение · AuditEvent", ["PK audit_id; FK binding_id", "actor, action, at, reason", "old_revision, new_revision", "request / decision / correction", "Документы — закрытые ссылки"])
    entity("assessment", 575, 970, "Оценка · Assessment", ["PK assessment_id; FK run_id", "state, score?; valid_until", "identification, registry_status", "method_snapshot, explanation", "Неизменяемый результат"])
    entity("fe", 1100, 970, "Основание факта · FactEvidence", ["PK evidence_id", "FK (fact_id, fact_revision)", "FK source_result_id", "external_ref, source_fragment", "Несколько оснований события"])
    entity("ae", 575, 1390, "Вклад · AssessmentEvidence", ["PK (assessment_id, fact_id)", "FK assessment_id", "FK (fact_id, fact_revision)", "factor_code, value, contribution", "explanation; один вклад события"])
    def rel(points, label, pos, left_count, left_pos, right_count, right_pos, dash=False):
        f.edge(points, label, pos, arrow=False, dash=dash)
        f.text(*left_pos, left_count, 20, bold=True)
        f.text(*right_pos, right_count, 20, bold=True)
    rel([(470, 250), (575, 250)], "история", (522, 231), "1", (486, 278), "0..N", (545, 278))
    rel([(995, 250), (1100, 250)], "субъект", (1048, 227), "0..N", (1020, 278), "1", (1082, 278))
    rel([(575, 320), (530, 320), (530, 490), (260, 490), (260, 550)], "запускает", (355, 473), "1", (550, 350), "0..N", (300, 530))
    rel([(470, 660), (575, 660)], "собирает", (522, 637), "1", (487, 690), "0..N", (545, 690))
    rel([(1310, 378), (1310, 550)], "имеет факты", (1400, 475), "1", (1275, 413), "0..N", (1270, 525))
    rel([(1310, 788), (1310, 970)], "подтверждается", (1410, 885), "1", (1277, 824), "1..N", (1270, 943))
    rel([(785, 788), (785, 875), (1045, 875), (1045, 1085), (1100, 1085)], "основания", (925, 855), "1", (820, 820), "0..N", (1060, 1120))
    rel([(470, 730), (520, 730), (520, 925), (650, 925), (650, 970)], "результат", (590, 905), "1", (493, 764), "0..1", (690, 952))
    rel([(575, 350), (505, 350), (505, 915), (260, 915), (260, 970)], "аудит", (355, 895), "1", (540, 381), "0..N", (303, 951))
    rel([(785, 1208), (785, 1390)], "объясняется", (893, 1300), "1", (748, 1245), "0..N", (740, 1362))
    rel([(1520, 665), (1545, 665), (1545, 1510), (995, 1510)], "учитывается", (1410, 1487), "1", (1532, 634), "0..N", (1035, 1541))
    f.note(50, 1390, 420, 235, ["Смена ЮЛ/ИП закрывает старую", "связь и создаёт новую.", "Указатель текущей оценки", "меняется атомарно вместе", "с проверкой версий задания.", "Другие поля и сущности", "агрегатора здесь опущены."], 21)
    f.text(50, 1700, ["FactEvidence хранит происхождение; AssessmentEvidence — влияние события на конкретную оценку.", "Период события сопоставляется с периодом связи; юридический факт остаётся фактом уровня ЮЛ/ИП."], 22, "start")
    f.save("03-er.svg")


def sequence():
    f = Figure(1570, 2120, "UML sequence · проверка, повтор и безопасная публикация", "Показаны проектные команды, а не действующие HTTP-методы; время идёт сверху вниз")
    xs = [155, 470, 785, 1100, 1415]
    labels = ["Клиентское\nприложение", "API модуля\nв Products", "База данных", "Worker\nпроверки", "Внешние\nисточники"]
    for x, name in zip(xs, labels):
        f.box(x-125, 120, 250, 85, name, GREY, 22, 0)
        f.edge([(x, 205), (x, 2030)], arrow=False, dash=True)
    def msg(i, j, y, label, reply=False):
        label_y = y - 16 - (len(label.split("\n")) - 1) * 26
        f.edge([(xs[i], y), (xs[j], y)], label, ((xs[i]+xs[j])/2, label_y), dash=reply)
    msg(0, 1, 270, "1. Реквизиты / перепроверка\n+ command_id")
    f.note(350, 305, 250, 78, "Права на точку;\nформат реквизитов", 20)
    msg(1, 2, 435, "2. В транзакции: версии,\ngeneration, задание")
    msg(2, 1, 510, "run_id; дубль → тот же run", True)
    msg(1, 0, 570, "3. Принято; статус проверки", True)
    msg(3, 2, 650, "4. Взять задание с lease")
    msg(2, 3, 715, "Снимок входов + lease_epoch", True)
    f.rect(935, 760, 610, 330, "none", dash=False)
    f.text(950, 789, "loop [для каждого разрешённого источника]", 20, "start", True)
    msg(3, 4, 850, "5. Запрос по точным\nидентификаторам и scope")
    msg(4, 3, 930, "Сведения / ошибка /\nнеоднозначность", True)
    f.note(970, 970, 540, 90, "Таймаут 10 с; не более 2 попыток.\nНеуспех сохраняется как недоступность,\nа не как отсутствие событий.", 20)
    f.note(925, 1130, 570, 105, "6. Сопоставить субъекта, объединить дубли;\nзафиксировать источники и конфигурацию;\nрассчитать допустимую оценку / причины null.", 21)
    msg(3, 2, 1300, "7. Сохранить результат с условием:\nversions + generation + lease_epoch")
    f.rect(625, 1330, 600, 325, "none")
    f.text(640, 1359, "alt [задание ещё имеет право публиковать]", 20, "start", True)
    f.text(925, 1404, "COMMIT: снимки, оценка, текущий указатель", 20)
    f.edge([(625, 1440), (1225, 1440)], arrow=False, dash=True)
    f.text(640, 1468, "[версии устарели, lease ещё принадлежит попытке]", 19, "start", True)
    f.text(925, 1510, "История / superseded; не менять текущий указатель", 20)
    f.edge([(625, 1540), (1225, 1540)], arrow=False, dash=True)
    f.text(640, 1568, "[lease / lease_epoch больше не принадлежат попытке]", 19, "start", True)
    f.text(925, 1612, "Отбросить ответ; не менять задание другой попытки", 20)
    msg(0, 1, 1775, "8. Открыть карточку\nили запросить статус")
    msg(1, 2, 1850, "9. Прочитать результат;\nпроверить версии и срок")
    msg(2, 1, 1925, "Безопасная проекция /\nнет актуального результата", True)
    msg(1, 0, 2000, "10. Факты, источники, даты,\nполнота и понятное объяснение", True)
    f.text(40, 2080, "Сплошные стрелки — запросы, пунктир — ответы. Долгая проверка не удерживает клиентский запрос.", 22, "start")
    f.save("04-sequence.svg")


def containers():
    f = Figure(1570, 1550, "C4 container · место модуля в Почини.Онлайн", "Целевая архитектура · контейнер C4 означает приложение, процесс или хранилище")
    f.rect(40, 300, 1490, 920, "none", 8, dash=True, stroke="#708096")
    f.text(60, 1197, "Почини.Онлайн · часть системы проверки", 22, "start", True)
    f.box(70, 130, 290, 100, "Автовладелец\n[человек]\nЧитает факты и оценку", GREY, 21)
    f.box(415, 130, 290, 110, "Представитель сервиса\n[человек]\nПодаёт реквизиты;\nзапрашивает исправления", GREY, 20)
    f.box(1195, 130, 290, 110, "Оператор\n[человек]\nРассматривает\nспорные сведения", GREY, 20)
    f.box(180, 395, 430, 130, "Client\n[приложение, TypeScript]\nКарточка клиента, реквизиты сервиса", BLUE, 22, 4)
    f.box(1150, 395, 335, 130, "Backoffice\n[веб-приложение]\nИнтерфейс оператора", BLUE, 22, 4)
    f.box(180, 650, 430, 130, "API Gateway\n[API, Python]\nМаршрутизация и сессия", BLUE, 22, 4)
    f.box(680, 650, 400, 160, "Products\n[API, Python]\nКаталог + новый модуль оценки;\nправа, версии, публичная проекция", BLUE, 21, 4)
    f.box(1150, 650, 335, 130, "Admin\n[API, Python]\nПрава и команды оператора", BLUE, 21, 4)
    f.box(180, 990, 430, 140, "БД домена Products\n[хранилище, PostgreSQL]\nСвязи, задания, снимки, оценки, аудит", BLUE, 21, 4)
    f.box(680, 990, 400, 140, "Worker проверки — новый\n[фоновый процесс, Python]\nТот же код домена; lease и адаптеры", GREEN, 21, 4)
    f.box(650, 1325, 820, 135, "Источники регистрационных и юридических сведений\n[внешние системы, сгруппированы]\nРеестр / поставщик данных, суды, разрешённые сведения об обращениях", GREY, 21, 4)
    f.edge([(215, 230), (215, 290), (300, 290), (300, 395)], "использует", (170, 365))
    f.edge([(560, 240), (560, 395)], "использует", (625, 280))
    f.edge([(1340, 240), (1340, 395)], "использует", (1400, 280))
    f.edge([(395, 525), (395, 650)], "HTTPS / JSON", (490, 595))
    f.edge([(1317, 525), (1317, 650)], "HTTPS / JSON", (1410, 595))
    f.edge([(610, 710), (680, 710)], "HTTP", (645, 691))
    f.edge([(1150, 710), (1080, 710)], "HTTP", (1116, 691))
    f.edge([(790, 810), (790, 890), (395, 890), (395, 990)], "SQL: задания и текущий результат", (550, 869))
    f.edge([(680, 1060), (610, 1060)], "SQL", (645, 1040))
    f.edge([(880, 1130), (880, 1325)], "HTTPS: запросы адаптеров\nОграничения поставщиков", (1160, 1254))
    f.note(1130, 925, 360, 220, "Источник недоступен —\nчастичный результат.\nДокументы и персональные\nданные не идут в публичную\nкарточку. Оценка не меняет\nправа управления профилем.", 21)
    f.text(50, 1498, "Синий — существующий контейнер с проектируемыми изменениями; зелёный — новый процесс; серый — участники и источники.", 21, "start")
    f.save("05-c4.svg")


if __name__ == "__main__":
    as_is()
    to_be()
    er_model()
    sequence()
    containers()
