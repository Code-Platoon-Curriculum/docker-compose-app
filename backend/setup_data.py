# exec(open("./setup_data.py").read())

from wine_api.models import Wine

Wine.objects.create(wine_name="Wood Shavings", price=25, varietal="Merlot", description="Savor the woodshop", img_url="https://via.placeholder.com/150/92c952")
Wine.objects.create(wine_name="Apple Muffins", price=35, varietal="Malbec", description="Fruity Dessert", img_url="https://via.placeholder.com/150/771796")
Wine.objects.create(wine_name="Trails", price=15, varietal="Zinfandel", description="Keep it in your camelback", img_url="https://via.placeholder.com/150/24f355")