#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
تطبيق مصاريفي - قاعدة 50/20/30
Masarify - 50/20/30 Budget App
Professional Arabic Expense Tracker
"""

import json
import os
from datetime import datetime, date
from kivy.clock import Clock
from kivy.utils import platform
from kivy.metrics import dp, sp
from kivy.core.text import LabelBase
from kivy.core.window import Window
from kivy.properties import StringProperty, NumericProperty, ObjectProperty, ListProperty, BooleanProperty

# Register Arabic font
FONT_PATH = os.path.join(os.path.dirname(__file__), "fonts", "NotoNaskhArabic-Regular.ttf")
if os.path.exists(FONT_PATH):
    LabelBase.register(name="Arabic", fn_regular=FONT_PATH)
else:
    # Fallback to bundled font location
    FONT_BUNDLED = "fonts/NotoNaskhArabic-Regular.ttf"
    if os.path.exists(FONT_BUNDLED):
        LabelBase.register(name="Arabic", fn_regular=FONT_BUNDLED)
    else:
        LabelBase.register(name="Arabic", fn_regular="Roboto")

from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.card import MDCard
from kivymd.uix.button import MDRaisedButton, MDFlatButton, MDRectangleFlatButton, MDFillRoundFlatButton, MDIconButton
from kivymd.uix.textfield import MDTextField
from kivymd.uix.label import MDLabel
from kivymd.uix.toolbar import MDTopAppBar
from kivymd.uix.bottomnavigation import MDBottomNavigation, MDBottomNavigationItem
from kivymd.uix.list import OneLineIconListItem, IconLeftWidget, TwoLineListItem, ThreeLineListItem
from kivymd.uix.dialog import MDDialog
from kivymd.uix.picker import MDDatePicker, MDTimePicker
from kivymd.uix.progressbar import MDCircularProgressBar
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.relativelayout import MDRelativeLayout
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.snackbar import MDSnackbar
from kivymd.uix.selectioncontrol import MDCheckbox
from kivy.uix.image import Image
from kivy.graphics import Color, RoundedRectangle, Rectangle, Line

# ─── Colors ─────────────────────────────────────────────────────────────────
TEAL = (0, 180, 160)
TEAL_HEX = "#00B4A0"
BLUE_NEEDS = (41, 128, 185)
BLUE_HEX = "#2980B9"
GREEN_SAVINGS = (39, 174, 96)
GREEN_HEX = "#27AE60"
ORANGE_WANTS = (230, 126, 34)
ORANGE_HEX = "#E67E22"
DARK_BG = (20, 25, 35)
DARK_CARD = (30, 38, 50)
WHITE = (255, 255, 255)
LIGHT_GRAY = (200, 200, 200)

# ─── Data Manager ───────────────────────────────────────────────────────────
DATA_FILE = os.path.join(os.path.expanduser("~"), ".masarify_data.json")

class DataManager:
    @staticmethod
    def load():
        default = {
            "monthly_income": 0.0,
            "currency": "SAR",
            "transactions": [],
            "theme": "dark",
            "budget_start_day": 1,
            "created_at": datetime.now().isoformat()
        }
        try:
            if os.path.exists(DATA_FILE):
                with open(DATA_FILE, "r", encoding="utf-8") as f:
                    return {**default, **json.load(f)}
        except:
            pass
        return default

    @staticmethod
    def save(data):
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    @staticmethod
    def get_current_month_transactions(data):
        now = datetime.now()
        year, month = now.year, now.month
        return [t for t in data["transactions"]
                if t.get("year") == year and t.get("month") == month]

    @staticmethod
    def get_category_totals(data):
        """Return total spent per category this month."""
        cats = {"needs": 0.0, "savings": 0.0, "wants": 0.0}
        now = datetime.now()
        for t in data["transactions"]:
            if t.get("type") == "expense" and t.get("year") == now.year and t.get("month") == now.month:
                cat = t.get("category", "wants")
                if cat in cats:
                    cats[cat] += float(t.get("amount", 0))
        return cats

    @staticmethod
    def get_budget_values(data):
        """Returns (needs_budget, savings_budget, wants_budget) based on income."""
        income = float(data.get("monthly_income", 0))
        return income * 0.50, income * 0.20, income * 0.30

    @staticmethod
    def add_transaction(data, trans):
        now = datetime.now()
        trans.update({
            "id": len(data["transactions"]) + 1,
            "year": now.year,
            "month": now.month,
            "day": now.day,
            "timestamp": now.isoformat()
        })
        data["transactions"].append(trans)
        DataManager.save(data)
        return data


# ─── Custom Widgets ─────────────────────────────────────────────────────────

class BudgetCircularProgress(MDCircularProgressBar):
    """Custom circular progress with label."""
    pass


class CategoryCard(MDCard):
    category = StringProperty("")
    title = StringProperty("")
    spent = NumericProperty(0)
    budget = NumericProperty(0)
    color = ListProperty([1, 1, 1, 1])
    icon = StringProperty("")

    def get_percent(self):
        if self.budget <= 0:
            return 0
        return min(100, (self.spent / self.budget) * 100)

    def get_remaining(self):
        return max(0, self.budget - self.spent)

    def get_status_text(self):
        pct = self.get_percent()
        if pct >= 100:
            return "⚠ تجاوزت الحد!"
        elif pct >= 80:
            return f"⚠ {100-pct:.0f}% متبقي"
        else:
            return f"✅ {self.get_remaining():.0f} ريال متبقي"


class TransactionItem(ThreeLineListItem):
    pass


# ─── Screens ─────────────────────────────────────────────────────────────────

class DashboardScreen(MDScreen):
    def on_enter(self):
        self.update_dashboard()

    def update_dashboard(self):
        app = MDApp.get_running_app()
        data = app.data

        income = float(data.get("monthly_income", 0))
        if income <= 0:
            self.ids.income_label.text = "⚠ حدد دخلك الشهري في الإعدادات"
            self.ids.income_label.theme_text_color = "Custom"
            self.ids.income_label.text_color = [1, 0.8, 0, 1]
            for cat in ["needs", "savings", "wants"]:
                self.ids[f"{cat}_card"].spent = 0
                self.ids[f"{cat}_card"].budget = 0
            return

        self.ids.income_label.text = f"💵 الدخل الشهري: {income:,.0f} ريال"
        self.ids.income_label.theme_text_color = "Custom"
        self.ids.income_label.text_color = [1, 1, 1, 1]

        needs_b, savings_b, wants_b = DataManager.get_budget_values(data)
        totals = DataManager.get_category_totals(data)

        self.ids.needs_card.spent = totals["needs"]
        self.ids.needs_card.budget = needs_b
        self.ids.savings_card.spent = totals["savings"]
        self.ids.savings_card.budget = savings_b
        self.ids.wants_card.spent = totals["wants"]
        self.ids.wants_card.budget = wants_b

        # Summary
        total_spent = sum(totals.values())
        remaining = income - total_spent
        self.ids.total_spent_label.text = f"إجمالي المصروف: {total_spent:,.0f} ريال"
        self.ids.remaining_label.text = f"المتبقي: {remaining:,.0f} ريال"
        if remaining < 0:
            self.ids.remaining_label.theme_text_color = "Error"
        else:
            self.ids.remaining_label.theme_text_color = "Custom"
            self.ids.remaining_label.text_color = [0.39, 0.91, 0.56, 1]  # Green


class AddExpenseScreen(MDScreen):
    def on_enter(self):
        self.ids.amount_field.text = ""
        self.ids.description_field.text = ""
        self.ids.category_menu.text = "اختر الفئة"
        self.selected_category = None
        self.transaction_type = "expense"

    selected_category = StringProperty("")
    transaction_type = StringProperty("expense")

    def open_category_menu(self):
        categories = [
            {"text": "🟦 احتياجات (50%)", "value": "needs"},
            {"text": "🟩 ادخار (20%)", "value": "savings"},
            {"text": "🟧 رغبات (30%)", "value": "wants"},
        ]
        menu_items = [
            {
                "text": cat["text"],
                "viewclass": "OneLineListItem",
                "on_release": lambda c=cat: self.select_category(c),
            }
            for cat in categories
        ]
        self.menu = MDDropdownMenu(
            caller=self.ids.category_menu,
            items=menu_items,
            width_mult=3,
        )
        self.menu.open()

    def select_category(self, cat):
        self.selected_category = cat["value"]
        self.ids.category_menu.text = cat["text"]
        self.menu.dismiss()

    def set_type_expense(self):
        self.transaction_type = "expense"
        self.ids.type_btn_expense.md_bg_color = [0.2, 0.6, 0.9, 1]
        self.ids.type_btn_expense.text_color = [1, 1, 1, 1]
        self.ids.type_btn_income.md_bg_color = [0.3, 0.3, 0.35, 1]
        self.ids.type_btn_income.text_color = [0.7, 0.7, 0.7, 1]

    def set_type_income(self):
        self.transaction_type = "income"
        self.ids.type_btn_income.md_bg_color = [0.2, 0.8, 0.4, 1]
        self.ids.type_btn_income.text_color = [1, 1, 1, 1]
        self.ids.type_btn_expense.md_bg_color = [0.3, 0.3, 0.35, 1]
        self.ids.type_btn_expense.text_color = [0.7, 0.7, 0.7, 1]

    def save_transaction(self):
        app = MDApp.get_running_app()
        amount_text = self.ids.amount_field.text.strip()
        description = self.ids.description_field.text.strip()

        if not amount_text:
            MDSnackbar(text="❌ أدخل المبلغ", snackbar_x="10dp", snackbar_y="10dp").open()
            return

        try:
            amount = float(amount_text.replace(",", ""))
        except:
            MDSnackbar(text="❌ المبلغ غير صحيح", snackbar_x="10dp", snackbar_y="10dp").open()
            return

        if amount <= 0:
            MDSnackbar(text="❌ المبلغ يجب أن يكون أكبر من صفر", snackbar_x="10dp", snackbar_y="10dp").open()
            return

        if self.transaction_type == "expense" and not self.selected_category:
            MDSnackbar(text="❌ اختر الفئة (احتياجات / ادخار / رغبات)", snackbar_x="10dp", snackbar_y="10dp").open()
            return

        trans = {
            "amount": amount,
            "description": description or "بدون وصف",
            "category": self.selected_category or "other",
            "type": self.transaction_type,
        }

        app.data = DataManager.add_transaction(app.data, trans)
        MDSnackbar(
            text="✅ تمت الإضافة بنجاح!",
            snackbar_x="10dp",
            snackbar_y="10dp",
            duration=2,
        ).open()

        # Reset form
        self.ids.amount_field.text = ""
        self.ids.description_field.text = ""
        self.ids.category_menu.text = "اختر الفئة"
        self.selected_category = None
        self.set_type_expense()

        # Update dashboard data
        app.root.get_screen("dashboard").update_dashboard()


class HistoryScreen(MDScreen):
    def on_enter(self):
        self.refresh_list()

    def refresh_list(self, filter_type="all", filter_category="all"):
        app = MDApp.get_running_app()
        data = app.data
        transactions = DataManager.get_current_month_transactions(data)

        # Sort by most recent first
        transactions.sort(key=lambda t: t.get("timestamp", ""), reverse=True)

        # Apply filters
        if filter_type != "all":
            transactions = [t for t in transactions if t.get("type") == filter_type]
        if filter_category != "all":
            transactions = [t for t in transactions if t.get("category") == filter_category]

        list_widget = self.ids.history_list
        list_widget.clear_widgets()

        if not transactions:
            list_widget.add_widget(
                MDLabel(
                    text="📭 لا توجد معاملات لهذا الشهر",
                    halign="center",
                    theme_text_color="Hint",
                    size_hint_y=None,
                    height=dp(100),
                )
            )
            return

        # Summary header
        total_expense = sum(t.get("amount", 0) for t in transactions if t.get("type") == "expense")
        total_income = sum(t.get("amount", 0) for t in transactions if t.get("type") == "income")

        header = MDCard(
            orientation="horizontal",
            size_hint_y=None,
            height=dp(60),
            md_bg_color=[0.25, 0.3, 0.42, 1],
            padding=dp(10),
        )
        header.add_widget(MDLabel(text=f"📤 مصروف: {total_expense:,.0f}", halign="center", theme_text_color="Error"))
        header.add_widget(MDLabel(text=f"📥 دخل: {total_income:,.0f}", halign="center", theme_text_color="Custom",
                                  text_color=[0.39, 0.91, 0.56, 1]))
        list_widget.add_widget(header)

        # Transaction items
        for t in transactions:
            amount = float(t.get("amount", 0))
            cat = t.get("category", "other")
            typ = t.get("type", "expense")
            desc = t.get("description", "")

            cat_icon = {"needs": "🏠", "savings": "💰", "wants": "🎮"}
            cat_name = {"needs": "احتياجات", "savings": "ادخار", "wants": "رغبات"}

            prefix = "🟢 +" if typ == "income" else "🔴 -"
            color = [0.39, 0.91, 0.56, 1] if typ == "income" else [1, 0.3, 0.3, 1]

            item = ThreeLineListItem(
                text=f"{prefix} {amount:,.0f} ريال",
                secondary_text=desc,
                tertiary_text=f"{cat_icon.get(cat, '📌')} {cat_name.get(cat, 'أخرى')} • {t.get('day', '?')}/{t.get('month', '?')}",
                theme_text_color="Custom",
                text_color=color,
            )
            list_widget.add_widget(item)


class SettingsScreen(MDScreen):
    def on_enter(self):
        app = MDApp.get_running_app()
        data = app.data
        income = float(data.get("monthly_income", 0))
        if income > 0:
            self.ids.income_field.text = f"{income:,.0f}"

    def save_income(self):
        app = MDApp.get_running_app()
        text = self.ids.income_field.text.strip()
        if not text:
            MDSnackbar(text="❌ أدخل الدخل الشهري", snackbar_x="10dp", snackbar_y="10dp").open()
            return
        try:
            income = float(text.replace(",", ""))
        except:
            MDSnackbar(text="❌ الرقم غير صحيح", snackbar_x="10dp", snackbar_y="10dp").open()
            return

        app.data["monthly_income"] = income
        DataManager.save(app.data)

        MDSnackbar(
            text=f"✅ تم حفظ الدخل: {income:,.0f} ريال",
            snackbar_x="10dp",
            snackbar_y="10dp",
        ).open()

        app.root.get_screen("dashboard").update_dashboard()

    def reset_data(self):
        dialog = MDDialog(
            title="⚠️ تأكيد الحذف",
            text="سيتم حذف جميع البيانات! هل أنت متأكد؟",
            buttons=[
                MDFlatButton(text="إلغاء", on_release=lambda x: dialog.dismiss()),
                MDFlatButton(
                    text="حذف الكل",
                    theme_text_color="Error",
                    on_release=lambda x: self.do_reset(dialog),
                ),
            ],
        )
        dialog.open()

    def do_reset(self, dialog):
        dialog.dismiss()
        app = MDApp.get_running_app()
        app.data = DataManager.load()  # reset to default
        app.data["transactions"] = []
        app.data["monthly_income"] = 0
        DataManager.save(app.data)
        self.ids.income_field.text = ""
        app.root.get_screen("dashboard").update_dashboard()
        app.root.get_screen("history").refresh_list()
        MDSnackbar(text="🗑️ تم حذف جميع البيانات", snackbar_x="10dp", snackbar_y="10dp").open()


# ─── Main App ─────────────────────────────────────────────────────────────────

class MasarifyApp(MDApp):
    data = ObjectProperty(None)

    def build(self):
        self.title = "مصاريفي - 50/20/30"
        self.theme_cls.primary_palette = "Teal"
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_hue = "600"

        self.data = DataManager.load()

        # Set app icon
        self.icon = os.path.expanduser("~/Masarify_icon.png")

        return self.root

    def on_start(self):
        # Auto-update dashboard on start
        Clock.schedule_once(lambda dt: self.update_all(), 0.5)

    def update_all(self):
        try:
            self.root.get_screen("dashboard").update_dashboard()
        except:
            pass


if __name__ == "__main__":
    MasarifyApp().run()
