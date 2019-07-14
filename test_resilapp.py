# -*- coding: latin_1 -*-
from lxml import html
import requests
import json
import unittest

class FlaskRequestsTests(unittest.TestCase):
    def test_Provinces(self):
        response_data = [
                        "ALAJUELA",
                        "CARTAGO",
                        "GUANACASTE",
                        "HEREDIA",
                        "LIMON",
                        "PUNTARENAS",
                        "SAN JOSE"
                        ]
        url = "https://resilapp.mybluemix.net/api/towns/provinces"
        resource=requests.get(url).json()
        self.assertEqual(response_data,resource)

    def test_Province_HEREDIA(self):
        response_data = [
                          "BARVA",
                          "BELEN",
                          "FLORES",
                          "HEREDIA",
                          "SAN ISIDRO",
                          "SAN PABLO",
                          "SAN RAFAEL",
                          "SANTA BARBARA",
                          "SANTO DOMINGO",
                          "SARAPIQUI"
                        ]
        url = "https://resilapp.mybluemix.net/api/towns/HEREDIA"
        resource=requests.get(url).json()
        self.assertEqual(response_data,resource)


    def test_Province_HEREDIA_Canton_BARVA(self):
        response_data = [
                          "BARVA",
                          "SAN ROQUE",
                          "SAN PEDRO",
                          "SAN PABLO",
                          "BUENAVISTA",
                          "SANTA LUCIA",
                          "PUENTE SALAS",
                          "SAN JOSE DE LA MONTAÑA",
                          "SAN MIGUEL",
                          "PORROSATI",
                          "SACRAMENTO",
                          "GALLITO"
                        ]
        url = "https://resilapp.mybluemix.net/api/towns/HEREDIA/BARVA"
        resource=requests.get(url).json()
        self.assertEqual(response_data,resource)

def main():
    unittest.main()
    return 0

if __name__ == '__main__':
    main()
