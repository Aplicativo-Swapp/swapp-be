from django.urls import reverse

from django.db import connection
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APITestCase

from .models import Category, PopularService

class HomeTest(TestCase):
    def setUp(self):
        Category.objects.create(name="Design e Tecnologia", slug="design_e_tecnologia", icon="swapp-fe/swapp_fe/src/assets/Design e Tecnologia.png")
        Category.objects.create(name="Consultoria", slug="consultoria", icon="swapp-fe/swapp_fe/src/assets/Consultoria.png")

        PopularService.objects.create(title="Corte de cabelo", location="Localização: Xique-Xique - BA", rating=4.5, reviews_count=10, image="swapp-fe/swapp_fe/src/assets/corte_de_cabelo.png")
        PopularService.objects.create(title="Pintura de parede", location="Localização: Jacareí - SP", rating=4.0, reviews_count=8, image="swapp-fe/swapp_fe/src/assets/pintura_de_parede.png")

    def test_categories_list(self):
        url = reverse('categories-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]['name'], "Design e Tecnologia")
        self.assertEqual(response.data[1]['name'], "Consultoria")
        self.assertEqual(response.data[0]['slug'], "design_e_tecnologia")
        self.assertEqual(response.data[1]['slug'], "consultoria")
        self.assertEqual(response.data[0]['icon'], "/swapp-fe/swapp_fe/src/assets/Design%20e%20Tecnologia.png")
        self.assertEqual(response.data[1]['icon'], "/swapp-fe/swapp_fe/src/assets/Consultoria.png")

    def test_popular_services_list(self):
        url = reverse('popular-services-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]['title'], "Corte de cabelo")
        self.assertEqual(response.data[1]['title'], "Pintura de parede")
        self.assertEqual(response.data[0]['location'], "Localização: Xique-Xique - BA")
        self.assertEqual(response.data[1]['location'], "Localização: Jacareí - SP")
        self.assertEqual(response.data[0]['rating'], '4.5')
        self.assertEqual(response.data[1]['rating'], '4.0')
        self.assertEqual(response.data[0]['reviews_count'], 10)
        self.assertEqual(response.data[1]['reviews_count'], 8)
        self.assertEqual(response.data[0]['image'], "/swapp-fe/swapp_fe/src/assets/corte_de_cabelo.png")
        self.assertEqual(response.data[1]['image'], "/swapp-fe/swapp_fe/src/assets/pintura_de_parede.png")