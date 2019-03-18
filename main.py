import json
import requests
import xlsxwriter

try:
    from BeautifulSoup import BeautifulSoup
except ImportError:
    from bs4 import BeautifulSoup


def add_header_dict(header, header_counter):
    if header not in headers_dict:
        headers_dict[header] = header_counter
        header_counter += 1
    return header_counter


def string_pre_processing(text):
    text = text.replace("[", "")
    text = text.replace("]", "")
    return text.replace("},{", "}\n{")


def html_parse(html_text, header_counter):
    # ' '.join(html_text.split())
    try:
        soup = BeautifulSoup(html_text, 'html.parser')
        # html = list(parsed_html.children)[2]
        # body = list(parsed_html.children)[3]

        tds = soup.find_all("td")
        if len(tds) == 0:
            #print("")
            return header_counter

        #print("### Details ###")
        for i in range(2, 8, 2):
            if i == 2:  # phone1
                info_dict['Phone-1'] = ' '.join(tds[i + 1].get_text().split())
                header_counter = add_header_dict('Phone-1', header_counter)
            # elif i == 8:  # phone2
            #     info_dict["Phone-2"] = ' '.join(tds[i + 1].get_text().split())
            #     header_counter = add_header_dict('Phone-2', header_counter)
            else:
                info_dict[' '.join(tds[i].get_text().split())] = ' '.join(tds[i + 1].get_text().split())
                header_counter = add_header_dict(' '.join(tds[i].get_text().split()), header_counter)
            #print("{}: {}".format(' '.join(tds[i].get_text().split()), ' '.join(tds[i + 1].get_text().split())))


        #for entrepreneur gets name surname of team
        tds = soup.find('i', {'class' : 'fa fa-users'}).parent.parent.find_all("td")
        for i in range(0, len(tds), 2):
            info_dict[' '.join(tds[i].get_text().split()) + " - " + str(int((i / 4) + 1))] = ' '.join(tds[i + 1].get_text().split())
            header_counter = add_header_dict(' '.join(tds[i].get_text().split()) + " - " + str(int((i / 4) + 1)), header_counter)
            #print("{}: {}".format(' '.join(tds[i].get_text().split()), ' '.join(tds[i + 1].get_text().split())))


        tds = soup.find(id="menu").find_all("td")
        for i in range(0, len(tds), 2):
            info_dict[' '.join(tds[i].get_text().split())] = ' '.join(tds[i + 1].get_text().split())
            header_counter = add_header_dict(' '.join(tds[i].get_text().split()), header_counter)
            #print("{}: {}".format(' '.join(tds[i].get_text().split()), ' '.join(tds[i + 1].get_text().split())))

        tds = soup.find(id="menu1").find_all("td")
        for i in range(0, len(tds), 2):
            info_dict[' '.join(tds[i].get_text().split())] = ' '.join(tds[i + 1].get_text().split())
            header_counter = add_header_dict(' '.join(tds[i].get_text().split()), header_counter)
            #print("{}: {}".format(' '.join(tds[i].get_text().split()), ' '.join(tds[i + 1].get_text().split())))

        # project details
        tds = soup.find(id="menu2").find_all("td")
        if len(tds) >= 5:
            for i in range(0, len(tds), 7):
                info_dict[' '.join(tds[i + 1].get_text().split()) + " - " + str(int((i / 7) + 1))] = ' '.join(
                    tds[i + 2].get_text().split())
                header_counter = add_header_dict(
                    ' '.join(tds[i + 1].get_text().split()) + " - " + str(int((i / 7) + 1)), header_counter)
                #print("{}: {}".format(' '.join(tds[i + 1].get_text().split()), ' '.join(tds[i + 2].get_text().split())))

                info_dict[' '.join(tds[i + 3].get_text().split()) + " - " + str(int((i / 7) + 1))] = ' '.join(
                    tds[i + 4].get_text().split())
                header_counter = add_header_dict(
                    ' '.join(tds[i + 3].get_text().split()) + " - " + str(int((i / 7) + 1)), header_counter)
                #print("{}: {}".format(' '.join(tds[i + 3].get_text().split()), ' '.join(tds[i + 4].get_text().split())))

                info_dict[' '.join(tds[i + 5].get_text().split()) + " - " + str(int((i / 7) + 1))] = ' '.join(
                    tds[i + 6].get_text().split())
                header_counter = add_header_dict(
                    ' '.join(tds[i + 5].get_text().split()) + " - " + str(int((i / 7) + 1)), header_counter)

        tds = soup.find(id="menu3").find_all("td")
        for i in range(0, len(tds), 2):
            info_dict[' '.join(tds[i].get_text().split())] = ' '.join(tds[i + 1].get_text().split())
            header_counter = add_header_dict(' '.join(tds[i].get_text().split()), header_counter)
            #print("{}: {}".format(' '.join(tds[i].get_text().split()), ' '.join(tds[i + 1].get_text().split())))

        tds = soup.find(id="menu4").find_all("td")
        for i in range(0, len(tds), 2):
            info_dict[' '.join(tds[i].get_text().split())] = ' '.join(tds[i + 1].get_text().split())
            header_counter = add_header_dict(' '.join(tds[i].get_text().split()), header_counter)
            #print("{}: {}".format(' '.join(tds[i].get_text().split()), ' '.join(tds[i + 1].get_text().split())))

        #print("\n")
        return header_counter

    except:
        #print("no details found ")
        return header_counter


# workbook = xlsxwriter.Workbook('techno-entrepreneur.xlsx')
workbook = xlsxwriter.Workbook('techno-entrepreneur.xlsx')
worksheet = workbook.add_worksheet()

info_dict = dict()
headers_dict = dict()
header_counter = 0
filename = "zeynep1.log"
#filename = "zeynep2.log"

with open(filename) as file:
    file_content = file.read()
    # print(file_content)

    # remove square brackets
    lines = string_pre_processing(file_content).splitlines()
    # print(lines)

    row = 1
    col = 0
    # each line is json
    for line in lines:
        # print(line)
        info_dict = dict()

        json_data = json.loads(line)
        # print(data)

        url = json_data["Url"]
        url = "http://technet.sanayi.gov.tr" + url
        # print(url)

        """
        print(
            "{}: {}\n{}: {}\n{}: {}\n{}: {}".format("Adi", json_data["Adi"], "Tip", json_data["Tip"], "Aciklama",
                                                    json_data["Aciklama"],
                                                    "Adres", json_data["Adres"]))
        """
        info_dict['Adi'] = json_data["Adi"]
        header_counter = add_header_dict("Adi", header_counter)

        info_dict["Tip"] = json_data["Tip"]
        header_counter = add_header_dict("Tip", header_counter)

        info_dict["Aciklama"] = json_data["Aciklama"]
        header_counter = add_header_dict("Aciklama", header_counter)

        info_dict["Adres"] = json_data["Adres"]
        header_counter = add_header_dict("Adres", header_counter)

        r = requests.get(url)
        html = r.content
        header_counter = html_parse(html, header_counter)

        for key in info_dict.keys():
            worksheet.write(row, headers_dict[key], info_dict[key])
            # row += 1
            # worksheet.write(row, col, key)
            # worksheet.write(row, col + 1, info_dict[key])

        row += 1
        print(row)
        #
        # if row > 10:
        #     for key in headers_dict:
        #         worksheet.write(0, headers_dict[key], key)
        #     workbook.close()

    for key in headers_dict:
        worksheet.write(0, headers_dict[key], key)
    workbook.close()

"""
filename = "zeynep.log"
with open(filename) as file:
    file_content = file.read()
    # print(file_content)

    # remove square brackets
    lines = string_pre_processing(file_content).splitlines()
    # print(lines)

    line = lines[3]
    json_data = json.loads(line)
    url = json_data["Url"]
    url = "http://technet.sanayi.gov.tr" + url
    #print_details(json_data)
    r = requests.get(url)
    html = r.content

soup = BeautifulSoup(html, 'html.parser')
# html = list(parsed_html.children)[2]
# body = list(parsed_html.children)[3]

tds = soup.find_all("td")
if len(tds) == 0:
    print("")


for i in range(2, 12, 2):
    print("{}: {}".format(' '.join(tds[i].get_text().split()), ' '.join(tds[i + 1].get_text().split())))

print("### Details ###")
tds = soup.find_all('td', id="menu2")
for i in range(0, len(tds), 5):
    print("{}: {}".format(' '.join(tds[i+1].get_text().split()), ' '.join(tds[i + 2].get_text().split())))
    print("{}: {}".format(' '.join(tds[i+3].get_text().split()), ' '.join(tds[i + 4].get_text().split())))

tds = soup.find_all('td', id="menu3")
for i in range(0, len(tds), 2):
    print("{}: {}".format(' '.join(tds[i].get_text().split()), ' '.join(tds[i + 1].get_text().split())))

tds = soup.find_all('td', id="menu4")
for i in range(0, len(tds), 2):
    print("{}: {}".format(' '.join(tds[i].get_text().split()), ' '.join(tds[i + 1].get_text().split())))

print("\n")

    except:
        print("no details found ")
        
"""
"""
1. url al
2. url ile içerik çek
3. içeriği parse et
4. gerekli alanları al
5. veri yapısına diğer bilgilerle ekle
6. file'a yeni bir line olarak ekle

"""
