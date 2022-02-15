#streamlit run C:/Users/becario/PycharmProjects/asin_tracker_app/venv/Lib/app.py
import streamlit as st
import urllib.request, csv, re, json, bs4
import pandas as pd

results = []

header=st.container()


with header:
    st.header('ASIN TRACKER')
    st.write('This app scans the detail page of every asin you give it')
    st.write('It will give you a CSV file as an output')
mercado = st.selectbox('Select the country',('USA', 'GERMANY', 'FRANCE', 'SPAIN', 'ITALY', 'UNITED KINGDOM'))
uploaded_file = st.file_uploader(label= "Choose a CSV file", type=['csv', 'xlsx'])

global df
if uploaded_file is not None:
    print(uploaded_file)
    print ("hello")
    #st.write(uploaded_file)
    st.write("File uploaded")
    try:
        df=pd.read_csv(uploaded_file, header=None)
        #csv = csv.reader(uploaded_file, delimiter=',')
    except Exception as e:
        print(e)
        df=pd.read_excel(uploaded_file, header=None)
df.columns = ['ASIN']
#st.write(df)
try:
    st.write(df)
except Exception as e:
    print(e)
    st.write("ERROR.Please upload file to the app")
csv = df['ASIN'].tolist()
st.text(csv)
for row in csv:
    asin = row
    if mercado == 'GERMANY':
        try:
            fp = urllib.request.Request(
                'https://www.amazon.{}/dp/{}'.format(mercado, asin),
                data=None,
                headers={
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36'
                }
            )
            content = urllib.request.urlopen(fp).read().decode('utf-8')
            soup = bs4.BeautifulSoup(content, features='html.parser')
        except:
            print('ERROR opening ' + asin)
        try:
            if re.search('class="a-size-base">(.*) Sternebewertungen</span>', content):
                result = re.search('class="a-size-base">(.*) Sternebewertungen</span>', content)
                ratings = result.group(1)
            else:
                result = re.search('class=\"a-size-base\">(.*) Sternebewertung</span>', content)
                ratings = result.group(1)
            result = re.search('class="a-icon-alt">(.*) von 5 Sternen</span>', content)
            stars = result.group(1)
            price = re.search('<span class="a-offscreen">(.*)</span><span aria-hidden="true">', content).group(1)

            if re.search('<span class="ac-badge-text-secondary ac-orange">Choice</span>', content):
                ac_label = "YES"
            else:
                ac_label = "NO"

            # <div id="shipFromSoldByAbbreviated_feature_div" class="celwidget" data-feature-name="shipFromSoldByAbbreviated" data-csa-c-id="jryzrl-gv34pe-bl46zf-ojjlwc" data-cel-widget="shipFromSoldByAbbreviated_feature_div"> <div id="sfsb_accordion_head" class="a-section show-on-unselected sfsb-header-text"> <div class="a-row"> <div class="a-column a-span12 a-text-left truncate"> <span class="a-size-small"> Versand durch: </span> <span class="a-size-small"> (.*) </span> </div> </div> <div class="a-row"> <div class="a-column a-span12 a-text-left truncate"> <span class="a-size-small"> Verkauft von: </span> <span class="a-size-small"> Amazon </span> </div> </div> </div> </div>

            if re.search('<span>Verkauf durch Amazon</span>', content):
                sold_by = "Amazon"
            elif re.search('<span>Verkauf durch (.*) </span>', content):
                sold_by = "Seller"
            else:
                sold_by = "not found"

            if re.search('<span>Versand durch Amazon</span>', content):
                sent_by = "Amazon"
            else:
                sent_by = "not found"

            return_obj = {
                'market': mercado,
                'asin': asin,
                'ratings': ratings,
                'stars': stars,
                'price': price,
                "Amazon`s Choice": ac_label,
                "Vendido por": sold_by,
                "Enviado por": sent_by
            }
        except:
            print(asin + ' ERROR. Saved as empty. Maybe it is not available')
            ratings = 0
            stars = 0
            return_obj = {
                'market': mercado,
                'asin': asin,
                'ratings': 'ERROR. Saved as empty. Maybe it is not available',
                'stars': "ERROR. Saved as empty. Maybe it is not available",
                'price': "ERROR. Saved as empty. Maybe it is not available",
                "Amazon`s Choice": "ERROR. Saved as empty. Maybe it is not available",
                "Vendido por": "ERROR. Saved as empty. Maybe it is not available",
                "Enviado por": "ERROR. Saved as empty. Maybe it is not available"
            }
        results.append(return_obj)
    elif mercado == 'FRANCE':
        try:
            fp = urllib.request.Request(
                'https://www.amazon.{}/dp/{}'.format(mercado, asin),
                data=None,
                headers={
                    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
                }
            )
            content = urllib.request.urlopen(fp).read().decode('utf-8')
            soup = bs4.BeautifulSoup(content, features='html.parser')
        except:
            print('ERROR opening ' + asin)

        try:
            if re.search('class=\"a-size-base\">(.*) évaluations</span>', content):
                result = re.search('class=\"a-size-base\">(.*) évaluations</span>', content)
                # print('Tipo empezando: ', type(result))
                ratings = result.group(1)
                ratings = float(ratings.replace('&nbsp;', '.'))
            else:
                result = re.search('class=\"a-size-base\">(.*) évaluation</span>', content)
                ratings = result.group(1)
                ratings = float(ratings.replace(',', '.'))
            result = soup.find('span', attrs={'class': 'a-icon-alt'})
            stars = result.get_text()
            stars = stars.replace(',', '.').replace('sur 5\xa0étoiles', '')
            stars = float(stars)
            price = re.search('<span class="a-offscreen">(.*)</span><span aria-hidden="true">', content).group(1)
            if re.search('<span class="ac-badge-text-secondary ac-orange">Choice</span>', content):
                ac_label = "YES"
            else:
                ac_label = "NO"
            return_obj = {
                'market': mercado,
                'asin': asin,
                'ratings': ratings,
                'stars': stars,
                'price': price,
                "Amazon's Choice": ac_label,
                'Vendido por': "not found",
                'Enviando por': "not found"
            }

        except:
            print(asin + ' ERROR. Saved as empty. Maybe it is not available')
            ratings = 0
            stars = 0
            return_obj = {
                'market': mercado,
                'asin': asin,
                'ratings': ratings,
                'stars': stars,
                'price': price,
                "Amazon's Choice": ac_label,
                'Vendido por': "Problema de codigo",
                'Enviando por': "Problema de codigo"
            }
        results.append(return_obj)
    elif mercado == 'ITALY':
        try:
            fp = urllib.request.Request(
                'https://www.amazon.{}/dp/{}'.format(mercado, asin),
                data=None,
                headers={
                    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
                }
            )
            content = urllib.request.urlopen(fp).read().decode('utf-8')
            soup = bs4.BeautifulSoup(content, features='html.parser')
        except:
            print('ERROR opening ' + asin)

        try:
            result = re.search('class="a-size-base">(.*) voti</span>', content)
            ratings = result.group(1)
            ratings = float(ratings.replace(',', '.').replace('&nbsp;', '.'))
            # result = soup.find('span', attrs={'class': 'a-icon-alt'})
            result = re.search('<span class=\"a-icon-alt\">(.*) su 5 stelle</span>', content)
            stars = result.group(1)
            stars = float(stars.replace(',', '.'))
            price = re.search('<span class="a-offscreen">(.*)</span><span aria-hidden="true">', content).group(1)
            if re.search('<span class="ac-badge-text-secondary ac-orange">Choice</span>', content):
                ac_label = "YES"
            else:
                ac_label = "NO"

            return_obj = {
                'market': mercado,
                'asin': asin,
                'ratings': ratings,
                'stars': stars,
                'price': price,
                "Amazon's Choice": ac_label,
                'Vendido por': "not found",
                'Enviando por': "not found"
            }

        except:
            print(asin + ' ERROR. Saved as empty. Maybe it is not available')
            ratings = 0
            stars = 0
            return_obj = {
                'market': mercado,
                'asin': asin,
                'ratings': ratings,
                'stars': stars,
                'price': 'price',
                "Amazon's Choice": 'ac_label',
                'Vendido por': "Problema de codigo",
                'Enviando por': "Problema de codigo"
            }
        results.append(return_obj)
    elif mercado == 'USA':
        try:
            fp = urllib.request.Request(
                'https://www.amazon.{}/dp/{}'.format(mercado, asin),
                data=None,
                headers={
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36'
                }
            )
            content = urllib.request.urlopen(fp).read().decode('utf-8')
            soup = bs4.BeautifulSoup(content, features='html.parser')
        except:
            print('ERROR opening ' + asin)
        try:
            if re.search('class=\"a-size-base\">(.*) ratings</span>', content):
                result = re.search('class=\"a-size-base\">(.*) ratings</span>', content)
                # print('Tipo empezando: ', type(result))
                ratings = result.group(1)
                ratings = float(ratings.replace(',', '.'))
                # print(ratings)
            else:
                result = re.search('class=\"a-size-base\">(.*) rating</span>', content)
                # print('Tipo empezando: ', type(result))
                ratings = result.group(1)
                ratings = float(ratings.replace(',', '.'))
                # print(ratings)
            result = re.search('<span class=\"a-icon-alt\">(.*) out of 5 stars</span>', content)
            stars = result.group(1)
            price = re.search('<span class="a-offscreen">(.*)</span><span aria-hidden="true">', content).group(1)
            if re.search('<span class="ac-badge-text-secondary ac-orange">Choice</span>', content):
                ac_label = "YES"
            else:
                ac_label = "NO"

            return_obj = {
                'market': mercado,
                'asin': asin,
                'ratings': ratings,
                'stars': stars,
                'price': price,
                "Amazon`s Choice": ac_label,
                "Vendido por": 'not found',
                "Enviado por": "not found"
            }
        except:
            print(asin + ' ERROR. Saved as empty. Maybe it is not available')
            ratings = 0
            stars = 0
            return_obj = {
                'market': 'ERROR. Saved as empty. Maybe it is not available',
                'asin': 'ERROR. Saved as empty. Maybe it is not available',
                'ratings': 'ERROR. Saved as empty. Maybe it is not available',
                'stars': "ERROR. Saved as empty. Maybe it is not available",
                'price': "ERROR. Saved as empty. Maybe it is not available",
                "Amazon`s Choice": "ERROR. Saved as empty. Maybe it is not available",
                "Vendido por": "ERROR. Saved as empty. Maybe it is not available",
                "Enviado por": "ERROR. Saved as empty. Maybe it is not available"
            }
        results.append(return_obj)

#f = open('C:/Users/becario/OneDrive - Brandhero/Escritorio/carpeta_resultados/resutados_prueba.json', 'w')
#f.write(json.dumps(results))
#f.close()
df = pd.DataFrame(results)
st.write(df)
#f=df.to_csv

#@st.cache
def convert_df(df):
    # IMPORTANT: Cache the conversion to prevent computation on every rerun
    return df.to_csv().encode('utf-8')

csv = convert_df(df)

st.download_button(
     label="Download data as CSV",
     data=csv,
     file_name='large_df.csv',
     mime='text/csv',
 )

print('Job finished. Exported to result.json')
print(len(results))

