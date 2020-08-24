import pytest

@pytest.mark.run(order=1)
def test_app_is_created(app):
    assert app.name == 'app'

@pytest.mark.run(order=2)
def test_config_is_development(config):

    assert config['ENV'] == 'Development'

@pytest.mark.run(order=3)
def test_sector_route(app):
    """
        Testing if sector route exists
    """
    assert 'sectors' in app.blueprints

@pytest.mark.run(order=4)
def test_products_route(app):
    """
        Testing if products route exists
    """
    assert 'products' in app.blueprints
