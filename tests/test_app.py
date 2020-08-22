def test_app_is_created(app):
    assert app.name == 'app'

def test_config_is_development(config):

    assert config['ENV'] == 'Development'

def test_sector_route(app):
    """
        Testing if sector route exists
    """
    assert 'sectors' in app.blueprints

def test_products_route(app):
    """
        Testing if products route exists
    """
    assert 'products' in app.blueprints
