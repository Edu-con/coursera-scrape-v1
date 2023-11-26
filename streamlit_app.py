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

        if len(courses) >= 5:
            break

    # Sort courses by review count in descending order
    courses.sort(key=lambda x: int(''.join(filter(str.isdigit, str(x[2])))), reverse=True)

    return courses

def get_course_info(site):
    source = requests.get(site).text
    soup = BeautifulSoup(source, 'lxml')

    try:
        title = soup.find('h1', class_='cds-119 cds-Typography-base css-1xy8ceb cds-121').text.strip()
        rating = soup.find('div', class_='cds-119 cds-Typography-base css-h1jogs cds-121').text.strip()

        # Extract review count and remove non-digit characters
        review_count = ''.join(filter(str.isdigit, soup.find('p', class_='cds-119 cds-Typography-base css-dmxkm1 cds-121').text.strip()))

        return title, rating, review_count, site

    except AttributeError:
        return None, None, None, None

def generate_html(courses):
    current_datetime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Streamlit Rendering
    st.title("Top 5 Coursera Courses")
    st.write(f"Last Updated on {current_datetime}")

    # Display courses in a table
    st.table(courses)

if __name__ == '__main__':
    courses = scrape_coursera()
    generate_html(courses)
