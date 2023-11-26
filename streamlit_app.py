import streamlit as st
import requests
from bs4 import BeautifulSoup
import datetime

def scrape_coursera():
    source = requests.get('https://www.coursera.org/sitemap~www~courses.xml').text
    soup = BeautifulSoup(source, 'xml')  # Use XML parser

    courses = []

    for site in soup.find_all('loc'):
        title, rating, review_count, course_link = get_course_info(site.text)
        if title and rating and review_count:
            courses.append((title, rating, review_count, course_link))

        if len(courses) >= 50:
            break

    # Sort courses by rating and then by review count (both in descending order)
    courses.sort(key=lambda x: (-float(x[1]), int(''.join(filter(str.isdigit, str(x[2]))))))

    return courses

def get_course_info(site):
    source = requests.get(site).text
    soup = BeautifulSoup(source, 'lxml')

    try:
        title = soup.find('h1', class_='cds-119 cds-Typography-base css-1xy8ceb cds-121').text.strip()
        rating = soup.find('div', class_='cds-119 cds-Typography-base css-h1jogs cds-121').text.strip()
        review_count = ''.join(filter(str.isdigit, soup.find('p', class_='cds-119 cds-Typography-base css-dmxkm1 cds-121').text.strip()))

        return title, rating, review_count, site

    except AttributeError:
        return None, None, None, None

def generate_html(courses):
    current_datetime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Streamlit Rendering
    st.title("Top 50 Coursera Courses")
    st.write(f"Last Updated on {current_datetime}")

    # Display courses in a Markdown-formatted table with clickable links
    markdown_table = "| Course Title | Rating |\n| --- | --- |\n"
    for title, rating, review_count, course_link in courses:
        markdown_table += f"| [{title}]({course_link}) | {rating} |\n"

    st.markdown(markdown_table, unsafe_allow_html=True)

if __name__ == '__main__':
    courses = scrape_coursera()
    generate_html(courses)