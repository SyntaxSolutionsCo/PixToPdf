import os

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.image import Image as KivyImage
from kivy.animation import Animation
from kivy.graphics import Color, RoundedRectangle, Rectangle
from kivy.metrics import dp, sp
from kivy.core.window import Window

from PIL import Image as PILImage


# ============================================================
# ANDROID / PLYER
# ============================================================

try:
    from jnius import autoclass
    from android.permissions import request_permissions, Permission

    ANDROID = True

except Exception:
    ANDROID = False


try:
    from plyer import filechooser

    PLYER_AVAILABLE = True

except Exception:
    PLYER_AVAILABLE = False


# ============================================================
# MODERN CARD
# ============================================================

class ModernCard(BoxLayout):

    def __init__(self, **kwargs):

        super().__init__(**kwargs)

        self.orientation = "vertical"

        # Responsive padding
        self.padding = [
            dp(16),
            dp(14),
            dp(16),
            dp(14)
        ]

        self.spacing = dp(8)

        self.size_hint_x = 1
        self.size_hint_y = None

        # Card automatski raste prema sadržaju
        self.bind(
            minimum_height=self.setter("height")
        )

        # Card background
        with self.canvas.before:

            Color(
                0.13,
                0.18,
                0.28,
                1
            )

            self.rect = RoundedRectangle(
                pos=self.pos,
                size=self.size,
                radius=[dp(18)]
            )

        self.bind(
            pos=self.update_rect,
            size=self.update_rect
        )


    def update_rect(self, *args):

        self.rect.pos = self.pos
        self.rect.size = self.size


# ============================================================
# GRADIENT STYLE BUTTON
# ============================================================

class GradientButton(Button):

    def __init__(
        self,
        button_color=(0.38, 0.30, 0.95, 1),
        **kwargs
    ):

        super().__init__(**kwargs)

        self.background_color = (
            0,
            0,
            0,
            0
        )

        self.color = (
            1,
            1,
            1,
            1
        )

        self.bold = True

        self.font_size = sp(17)

        self.size_hint_x = 1
        self.size_hint_y = None

        self.height = dp(52)

        self.padding = [
            dp(10),
            dp(5)
        ]

        # Button background
        with self.canvas.before:

            Color(
                *button_color
            )

            self.rect = RoundedRectangle(
                pos=self.pos,
                size=self.size,
                radius=[dp(14)]
            )

        self.bind(
            pos=self.update_rect,
            size=self.update_rect
        )

        self.bind(
            state=self.on_press_anim
        )


    def update_rect(self, *args):

        self.rect.pos = self.pos
        self.rect.size = self.size


    def on_press_anim(
        self,
        instance,
        value
    ):

        if value == "down":

            Animation(
                opacity=0.8,
                duration=0.1,
                t="out_quad"
            ).start(self)

        else:

            Animation(
                opacity=1.0,
                duration=0.1,
                t="out_quad"
            ).start(self)


# ============================================================
# MAIN APP
# ============================================================

class PixToPdfApp(App):

    def build(self):

        self.title = "PixToPdf"

        self.selected_file_path = ""

        self.last_pdf_path = ""


        # ====================================================
        # ANDROID PERMISSIONS
        # ====================================================

        if ANDROID:

            try:

                request_permissions(
                    [
                        Permission.READ_EXTERNAL_STORAGE,
                        Permission.WRITE_EXTERNAL_STORAGE,
                        Permission.READ_MEDIA_IMAGES
                    ]
                )

            except Exception:

                pass


        # ====================================================
        # ROOT
        # ====================================================

        root = AnchorLayout(
            anchor_x="center",
            anchor_y="top"
        )


        # Background
        with root.canvas.before:

            Color(
                0.07,
                0.09,
                0.15,
                1
            )

            self.bg_rect = Rectangle(
                pos=root.pos,
                size=root.size
            )


        root.bind(
            pos=lambda instance, value:
                setattr(
                    self.bg_rect,
                    "pos",
                    value
                ),

            size=lambda instance, value:
                setattr(
                    self.bg_rect,
                    "size",
                    value
                )
        )


        # ====================================================
        # SCROLL VIEW
        # ====================================================

        scroll = ScrollView(

            size_hint=(
                1,
                1
            ),

            do_scroll_x=False,

            do_scroll_y=True,

            bar_width=dp(3),

            scroll_type=[
                "content"
            ]
        )


        # ====================================================
        # MAIN CONTENT
        # ====================================================

        main_layout = BoxLayout(

            orientation="vertical",

            padding=[
                dp(14),
                dp(22),
                dp(14),
                dp(24)
            ],

            spacing=dp(14),

            size_hint_x=1,

            size_hint_y=None
        )


        main_layout.bind(

            minimum_height=
            main_layout.setter(
                "height"
            )

        )


        # ====================================================
        # HEADER
        # ====================================================

        header_layout = BoxLayout(

            orientation="horizontal",

            size_hint_x=1,

            size_hint_y=None,

            height=dp(58),

            spacing=dp(12)
        )


        # ====================================================
        # LOGO
        # ====================================================

        if os.path.exists("icon.png"):

            logo_img = KivyImage(

                source="icon.png",

                size_hint=(
                    None,
                    None
                ),

                size=[
                    dp(48),
                    dp(48)
                ],

                allow_stretch=True,

                keep_ratio=True
            )

            header_layout.add_widget(
                logo_img
            )


        # ====================================================
        # TITLE BOX
        # ====================================================

        title_box = BoxLayout(

            orientation="vertical",

            spacing=dp(1),

            size_hint_x=1,

            size_hint_y=None,

            height=dp(54)
        )


        # APP TITLE

        app_title = Label(

            text="PixToPdf",

            font_size=sp(24),

            bold=True,

            color=(
                1,
                1,
                1,
                1
            ),

            halign="left",

            valign="middle",

            size_hint_x=1,

            size_hint_y=None,

            height=dp(30),

            shorten=True,

            shorten_from="right"
        )


        app_title.bind(

            size=lambda instance, value:

            setattr(

                instance,

                "text_size",

                (
                    value[0],
                    None
                )

            )

        )


        # SUBTITLE

        app_subtitle = Label(

            text="Convert images to professional PDF",

            font_size=sp(12),

            color=(
                0.58,
                0.63,
                0.73,
                1
            ),

            halign="left",

            valign="middle",

            size_hint_x=1,

            size_hint_y=None,

            height=dp(22),

            shorten=True,

            shorten_from="right"
        )


        app_subtitle.bind(

            size=lambda instance, value:

            setattr(

                instance,

                "text_size",

                (
                    value[0],
                    None
                )

            )

        )


        title_box.add_widget(
            app_title
        )

        title_box.add_widget(
            app_subtitle
        )


        header_layout.add_widget(
            title_box
        )


        main_layout.add_widget(
            header_layout
        )


        # ====================================================
        # SELECT IMAGE BUTTON
        # ====================================================

        self.btn_select = GradientButton(

            text="Select Image to Convert",

            button_color=(
                0.38,
                0.30,
                0.95,
                1
            )
        )


        self.btn_select.bind(

            on_release=
            self.open_gallery

        )


        main_layout.add_widget(
            self.btn_select
        )


        # ====================================================
        # PREVIEW CARD
        # ====================================================

        card_preview = ModernCard()


        lbl_preview_title = Label(

            text="Selected File Info",

            font_size=sp(12),

            color=(
                0.58,
                0.63,
                0.73,
                1
            ),

            halign="left",

            valign="middle",

            size_hint_x=1,

            size_hint_y=None,

            height=dp(22)
        )


        lbl_preview_title.bind(

            size=lambda instance, value:

            setattr(

                instance,

                "text_size",

                (
                    value[0],
                    None
                )

            )

        )


        card_preview.add_widget(
            lbl_preview_title
        )


        self.lbl_selected_file = Label(

            text="No image selected yet",

            font_size=sp(14),

            color=(
                0.85,
                0.88,
                0.93,
                1
            ),

            halign="left",

            valign="middle",

            size_hint_x=1,

            size_hint_y=None,

            height=dp(30),

            shorten=True,

            shorten_from="right"
        )


        self.lbl_selected_file.bind(

            size=lambda instance, value:

            setattr(

                instance,

                "text_size",

                (
                    value[0],
                    None
                )

            )

        )


        card_preview.add_widget(
            self.lbl_selected_file
        )


        main_layout.add_widget(
            card_preview
        )


        # ====================================================
        # OUTPUT FILENAME CARD
        # ====================================================

        card_name = ModernCard()


        lbl_name = Label(

            text="Output PDF File Name",

            font_size=sp(12),

            color=(
                0.58,
                0.63,
                0.73,
                1
            ),

            halign="left",

            valign="middle",

            size_hint_x=1,

            size_hint_y=None,

            height=dp(22)
        )


        lbl_name.bind(

            size=lambda instance, value:

            setattr(

                instance,

                "text_size",

                (
                    value[0],
                    None
                )

            )

        )


        card_name.add_widget(
            lbl_name
        )


        # ====================================================
        # TEXT INPUT
        # ====================================================

        self.input_name = TextInput(

            text="document.pdf",

            font_size=sp(15),

            multiline=False,

            size_hint_x=1,

            size_hint_y=None,

            height=dp(46),

            padding=[
                dp(12),
                dp(10)
            ],

            background_color=(
                0.09,
                0.12,
                0.19,
                1
            ),

            foreground_color=(
                1,
                1,
                1,
                1
            ),

            cursor_color=(
                0.38,
                0.30,
                0.95,
                1
            ),

            hint_text_color=(
                0.5,
                0.55,
                0.65,
                1
            ),

            write_tab=False
        )


        card_name.add_widget(
            self.input_name
        )


        main_layout.add_widget(
            card_name
        )


        # ====================================================
        # CONVERT BUTTON
        # ====================================================

        self.btn_convert = GradientButton(

            text="Convert to PDF",

            button_color=(
                0.38,
                0.30,
                0.95,
                1
            )
        )


        self.btn_convert.bind(

            on_release=
            self.convert_images_to_pdf

        )


        main_layout.add_widget(
            self.btn_convert
        )


        # ====================================================
        # SAVE BUTTON
        # ====================================================

        self.btn_save = GradientButton(

            text="Save to Gallery",

            button_color=(
                0.11,
                0.63,
                0.53,
                1
            )
        )


        self.btn_save.bind(

            on_release=
            self.save_to_gallery

        )


        main_layout.add_widget(
            self.btn_save
        )


        # ====================================================
        # STATUS CARD
        # ====================================================

        card_status = ModernCard()


        lbl_status_title = Label(

            text="Status",

            font_size=sp(12),

            color=(
                0.58,
                0.63,
                0.73,
                1
            ),

            halign="left",

            valign="middle",

            size_hint_x=1,

            size_hint_y=None,

            height=dp(22)
        )


        lbl_status_title.bind(

            size=lambda instance, value:

            setattr(

                instance,

                "text_size",

                (
                    value[0],
                    None
                )

            )

        )


        card_status.add_widget(
            lbl_status_title
        )


        self.status_label = Label(

            text="Ready to work.",

            font_size=sp(14),

            color=(
                0.40,
                0.86,
                0.65,
                1
            ),

            halign="left",

            valign="middle",

            size_hint_x=1,

            size_hint_y=None,

            height=dp(30),

            shorten=True,

            shorten_from="right"
        )


        self.status_label.bind(

            size=lambda instance, value:

            setattr(

                instance,

                "text_size",

                (
                    value[0],
                    None
                )

            )

        )


        card_status.add_widget(
            self.status_label
        )


        main_layout.add_widget(
            card_status
        )


        # ====================================================
        # ADD CONTENT TO SCROLL
        # ====================================================

        scroll.add_widget(
            main_layout
        )


        root.add_widget(
            scroll
        )


        return root


    # ========================================================
    # OPEN GALLERY
    # ========================================================

    def open_gallery(
        self,
        instance
    ):

        if PLYER_AVAILABLE:

            try:

                filechooser.open_file(

                    title="Select Image",

                    filters=[
                        (
                            "Image files",
                            "*.png;*.jpg;*.jpeg;*.bmp;*.webp"
                        )
                    ],

                    multiple=False,

                    on_selection=
                    self.handle_selection

                )

            except Exception as e:

                self.status_label.text = (
                    f"Error opening gallery: {str(e)}"
                )

                self.status_label.color = (
                    0.95,
                    0.38,
                    0.38,
                    1
                )

        else:

            self.status_label.text = (
                "File chooser not available."
            )

            self.status_label.color = (
                0.95,
                0.38,
                0.38,
                1
            )


    # ========================================================
    # HANDLE IMAGE SELECTION
    # ========================================================

    def handle_selection(
        self,
        selection
    ):

        if selection:

            self.selected_file_path = (
                selection[0]
            )

            file_name_only = os.path.basename(
                self.selected_file_path
            )


            self.lbl_selected_file.text = (
                f"✓ {file_name_only}"
            )


            self.lbl_selected_file.color = (
                0.40,
                0.86,
                0.65,
                1
            )


            self.status_label.text = (
                "Image selected successfully."
            )


            self.status_label.color = (
                0.40,
                0.86,
                0.65,
                1
            )


    # ========================================================
    # CONVERT IMAGE TO PDF
    # ========================================================

    def convert_images_to_pdf(
        self,
        instance
    ):

        path = (
            self.selected_file_path
        )

        pdf_name = (
            self.input_name.text.strip()
        )


        if not path or not os.path.exists(path):

            self.status_label.text = (
                "Error: Please select an image first."
            )

            self.status_label.color = (
                0.95,
                0.38,
                0.38,
                1
            )

            return


        if not pdf_name:

            self.status_label.text = (
                "Error: Please enter output PDF file name."
            )

            self.status_label.color = (
                0.95,
                0.38,
                0.38,
                1
            )

            return


        # Dodaj .pdf ako korisnik nije uneo ekstenziju

        if not pdf_name.lower().endswith(
            ".pdf"
        ):

            pdf_name += ".pdf"


        try:

            pil_images = []


            img = PILImage.open(
                path
            )


            if img.mode != "RGB":

                img = img.convert(
                    "RGB"
                )


            pil_images.append(
                img
            )


            # =================================================
            # OUTPUT DIRECTORY
            # =================================================

            if ANDROID:

                output_dir = (
                    "/sdcard/Download"
                )

            else:

                output_dir = os.getcwd()


                if not os.path.exists(
                    output_dir
                ):

                    os.makedirs(
                        output_dir,
                        exist_ok=True
                    )


            output_path = os.path.join(

                output_dir,

                pdf_name

            )


            # =================================================
            # SAVE PDF
            # =================================================

            if len(pil_images) > 0:

                pil_images[0].save(

                    output_path,

                    "PDF",

                    save_all=True,

                    append_images=
                    pil_images[1:]

                )


            self.last_pdf_path = (
                output_path
            )


            self.status_label.text = (

                f"Successfully created: "
                f"{output_path}"

            )


            self.status_label.color = (
                0.40,
                0.86,
                0.65,
                1
            )


        except Exception as e:

            self.status_label.text = (

                f"Conversion error: "
                f"{str(e)}"

            )


            self.status_label.color = (
                0.95,
                0.38,
                0.38,
                1
            )


    # ========================================================
    # SAVE TO GALLERY
    # ========================================================

    def save_to_gallery(
        self,
        instance
    ):

        try:

            if (

                hasattr(
                    self,
                    "last_pdf_path"
                )

                and

                os.path.exists(
                    self.last_pdf_path
                )

            ):

                self.status_label.text = (

                    f"Saved: "
                    f"{self.last_pdf_path}"

                )


                self.status_label.color = (
                    0.40,
                    0.86,
                    0.65,
                    1
                )


                # =============================================
                # ANDROID MEDIA SCANNER
                # =============================================

                if ANDROID:

                    try:

                        PythonActivity = autoclass(

                            "org.kivy.android."
                            "PythonActivity"

                        )


                        Intent = autoclass(

                            "android.content.Intent"

                        )


                        Uri = autoclass(

                            "android.net.Uri"

                        )


                        File = autoclass(

                            "java.io.File"

                        )


                        f = File(

                            self.last_pdf_path

                        )


                        uri = Uri.fromFile(
                            f
                        )


                        scanIntent = Intent(

                            Intent
                            .ACTION_MEDIA_SCANNER_SCAN_FILE,

                            uri

                        )


                        PythonActivity.mActivity.sendBroadcast(

                            scanIntent

                        )


                    except Exception:

                        pass


            else:

                self.status_label.text = (

                    "Please convert images "
                    "to PDF first."

                )


                self.status_label.color = (
                    0.95,
                    0.38,
                    0.38,
                    1
                )


        except Exception as e:

            self.status_label.text = (

                f"Save error: "
                f"{str(e)}"

            )


            self.status_label.color = (
                0.95,
                0.38,
                0.38,
                1
            )


# ============================================================
# RUN APP
# ============================================================

if __name__ == "__main__":

    PixToPdfApp().run()