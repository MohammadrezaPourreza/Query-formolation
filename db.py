import mysql.connector
from dotenv import load_dotenv
from os import getenv
from utils import remove_parenthesis
from typing import Iterable, Tuple, List

load_dotenv()
cnx = mysql.connector.connect(
    host="172.18.28.17",
    user="root",
    password="Kholmed@ng98",
    database="umls",
)


def get_cui_str(cui: str, prefered=True, no_parenthesis=True) -> str:
    query = "SELECT STR, ISPREF FROM MRCONSO WHERE CUI = %s"
    cursor = cnx.cursor()
    cursor.execute(query, (cui,))

    for result in cursor.fetchall():
        if prefered:
            if result[1] == "Y":
                return remove_parenthesis(result[0]) if no_parenthesis else result[0]
        else:
            return remove_parenthesis(result[0]) if no_parenthesis else result[0]
    return None


def get_list_of_cui(
    cui: Iterable[str], prefered=True, no_parenthesis=True
) -> List[Tuple[str, str]]:
    pass


if __name__ == "__main__":
    print(get_cui_str("C0684249", no_parenthesis=False))
    print(get_cui_str("C1306460", no_parenthesis=False))
    print(get_cui_str("C0242379", no_parenthesis=False))
