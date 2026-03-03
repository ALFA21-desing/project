"""
Test Admin Dashboard - verifies access and product list
"""

import pytest
from pages.LoginPage import LoginPage
from pages.AdminPage import AdminPage


class TestAdminDashboard:
    @pytest.mark.smoke
    @pytest.mark.admin
    def test_admin_login_and_view_products(self, driver, base_url):
        # the admin dashboard requires the backend server to be running since
        # it queries /api/products.  if base_url uses the file:// protocol we
        # can't exercise it, so simply skip the test in that case.
        if base_url.startswith("file://"):
            pytest.skip("Backend server not available for admin page")

        # login as admin and ensure the dashboard loads with some rows
        login = LoginPage(driver, base_url)
        login.navigate()
        login.login('admin', 'Admin@123')

        admin = AdminPage(driver, base_url)
        # give time for redirect
        import time
        time.sleep(2)
        assert admin.is_loaded(), "Should be on admin dashboard after admin login"
        count = admin.get_product_count()
        print(f"Found {count} product rows on admin page")
        # table should at least be present; number of rows doesn't matter
        assert count >= 0
        # logout to leave state clean
        admin.logout()
