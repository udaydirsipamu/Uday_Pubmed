import requests
import xml.etree.ElementTree as ET
import csv
import argparse
import re
from bs4 import BeautifulSoup

PUBMED_BASE_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
PUBMED_FETCH_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"

def fetch_papers(query, debug=False):
    search_params = {
        "db": "pubmed",
        "term": query,
        "retmax": 10,
        "retmode": "xml"
    }
    
    search_response = requests.get(PUBMED_BASE_URL, params=search_params)
    search_soup = BeautifulSoup(search_response.content, "xml")
    paper_ids = [id_tag.text for id_tag in search_soup.find_all("Id")]

    if not paper_ids:
        print("No papers found.")
        return []

    fetch_params = {
        "db": "pubmed",
        "id": ",".join(paper_ids),
        "retmode": "xml"
    }
    
    fetch_response = requests.get(PUBMED_FETCH_URL, params=fetch_params)
    fetch_soup = BeautifulSoup(fetch_response.content, "xml")

    papers = []
    
    for article in fetch_soup.find_all("PubmedArticle"):
        pubmed_id = article.PubmedData.ArticleIdList.find("ArticleId", {"IdType": "pubmed"}).text
        
        title_tag = article.find("ArticleTitle")
        title = title_tag.text if title_tag else "N/A"

        pub_date = article.find("PubDate")
        day = pub_date.Day.text if pub_date and pub_date.find("Day") else "01"
        month = pub_date.Month.text if pub_date and pub_date.find("Month") else "01"
        year = pub_date.Year.text if pub_date and pub_date.find("Year") else "0000"
        publication_date = f"{day}-{month}-{year}" if year != "0000" else "N/A"

        authors = []
        company_affiliations = []
        corresponding_email = "N/A"

        for author in article.find_all("Author"):
            lastname = author.LastName.text if author.find("LastName") else ""
            forename = author.ForeName.text if author.find("ForeName") else ""
            initials = f"{forename[0]}. " if forename else ""
            full_name = f"{initials}{lastname}".strip()
            
            if full_name:
                authors.append(full_name)

            affiliation_info = author.find_next("AffiliationInfo")
            if affiliation_info:
                affiliation_text = affiliation_info.text
                company_affiliations.append(affiliation_text)

                email_match = re.search(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", affiliation_text)
                if email_match:
                    corresponding_email = email_match.group(0)

        correspondence = article.find("CommentsCorrections", {"RefType": "Correspondence"})
        if correspondence:
            email_match = re.search(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", correspondence.text)
            if email_match:
                corresponding_email = email_match.group(0)

        company_affiliations = company_affiliations[:2]

        paper_data = {
            "PubMedID": pubmed_id,
            "Title": title,
            "Publication Date": publication_date,
            "Non-academic Author(s)": ", ".join(authors) if authors else "N/A",
            "Company Affiliation(s)": ", ".join(company_affiliations) if company_affiliations else "N/A",
            "Corresponding Author Email": corresponding_email
        }

        papers.append(paper_data)

        if debug:
            print(paper_data)

    return papers

def save_to_csv(papers, filename):
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=["PubMedID", "Title", "Publication Date", "Non-academic Author(s)", "Company Affiliation(s)", "Corresponding Author Email"])
        writer.writeheader()
        writer.writerows(papers)
    print(f"Results saved to {filename}")

def main():
    parser = argparse.ArgumentParser(description="Fetch papers from PubMed based on a query.")
    parser.add_argument("query", type=str, help="Search query for PubMed")
    parser.add_argument("-d", "--debug", action="store_true", help="Enable debug mode to print results in console")
    parser.add_argument("-f", "--file", type=str, help="Save results to a CSV file")
    
    args = parser.parse_args()
    papers = fetch_papers(args.query, args.debug)
    
    if args.file:
        save_to_csv(papers, args.file)
    else:
        for paper in papers:
            print(paper)

if __name__ == "__main__":
    main()
