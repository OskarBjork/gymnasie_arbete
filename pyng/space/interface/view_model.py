from math import ceil

import pygame
import pygame_gui
from pygame import Surface

from pyng.config import RED, BLACK, WHITE, GRID_SCALE, PIXELS_PER_METER, ORIGIN
from pyng.space.vectors import Vector2D


# TODO: Flytta


def convert_coordinates(screen, x, y) -> (float, float):
    return x, screen.get_height() - y


def relative_to_origin(position_vector):
    return position_vector + Vector2D(*ORIGIN)


class ViewModel:
    def __init__(self, screen: Surface, ui_manager) -> None:
        self.screen = screen
        self.width = screen.get_width()
        self.height = screen.get_height()
        self.ui_manager = ui_manager
        self.font = pygame.font.Font(None, 36)

        self.ui_mode = True  # True om i spawn läge
        self.shape = "circle"
        self.tool = "force"

    def convert_coordinates(self, x, y) -> (float, float):
        return x, self.screen.get_height() - y

    def clear(self):
        self.screen.fill(WHITE)

    def update(self, ui_refresh_rate: float):
        pygame.display.update()
        self.ui_manager.update(ui_refresh_rate)

    def place_pixel(self, x: int, y: int, color: tuple) -> None:
        converted_x, converted_y = self.convert_coordinates(x, y)
        pygame.draw.rect(self.screen, color, (converted_x, converted_y, 1, 1))

    def show_grid(self):
        origin = ORIGIN

        num_of_lines_vertical = ceil(self.width / PIXELS_PER_METER)
        num_of_lines_horizontal = ceil(self.height / PIXELS_PER_METER)

        # Skapar rutorna
        for i in range(num_of_lines_vertical):
            x_offset = i * PIXELS_PER_METER

            pygame.draw.line(
                surface=self.screen,
                color=BLACK,
                start_pos=self.convert_coordinates(origin[0] + x_offset, origin[1]),
                end_pos=self.convert_coordinates(origin[0] + x_offset, self.height),
            )
            # Ritar siffrorna
            self.render_text(
                f"{i * 100}",
                BLACK,
                self.convert_coordinates(origin[0] + x_offset, origin[1]),
                20,
            )

        # Samma ordning som ovan
        for i in range(num_of_lines_horizontal):
            y_offset = i * PIXELS_PER_METER

            pygame.draw.line(
                surface=self.screen,
                color=BLACK,
                start_pos=self.convert_coordinates(origin[0], origin[1] + y_offset),
                end_pos=self.convert_coordinates(self.width, origin[1] + y_offset),
            )

            if i == 0:
                continue
            self.render_text(
                f"{i * 100}",
                BLACK,
                self.convert_coordinates(origin[0] - 50, origin[1] + y_offset),
                20,
            )
        if self.ui_mode == True:  # visar all text som ska vara på spawner skärmen
            self.render_text(
                "Spawner",
                BLACK,
                (10, 20),
                60,
            )

            self.render_text(
                "x-coordinate:",
                BLACK,
                (5, 218),
                15,
            )

            self.render_text(
                "y-coordinate:",
                BLACK,
                (5 + 0.35 * ORIGIN[0], 218),
                15,
            )

            if self.shape == "circle":
                self.render_text(
                    "Radius:",
                    BLACK,
                    (5, 350),
                    20,
                )

                self.render_text(
                    "Mass:",
                    BLACK,
                    (5, 450),
                    20,
                )

        if self.ui_mode == False:  # visar all text som ska vara på manipulate skärmen
            self.render_text(
                "Manipulate",
                BLACK,
                (10, 20),
                60,
            )
            match self.tool:
                case "move":
                    pass

                case "force":
                    self.render_text(
                        "Force [Newton]:",
                        BLACK,
                        (10, 245),
                        20,
                    )

                    self.render_text(
                        "Angle [rad]:",
                        BLACK,
                        (10, 335),
                        20,
                    )

                case "velocity":
                    self.render_text(
                        "Velocity [m/s]:",
                        BLACK,
                        (10, 245),
                        20,
                    )

                    self.render_text(
                        "Angle [rad]:",
                        BLACK,
                        (10, 335),
                        20,
                    )

    def render_ui(self, ui_manager):
        self.show_grid()
        ui_manager.draw_ui(self.screen)

    def show_mode_buttons(self, square_image):
        pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((0, -50), (0.33 * ORIGIN[0], 45)),
            text="Manipulate",
            manager=self.ui_manager,
            object_id="#manipulate_view_changer_button",
            anchors={"left": "left", "bottom": "bottom"},
        )

        pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(
                (5 + 0.33 * ORIGIN[0], -50), (0.33 * ORIGIN[0], 45)
            ),
            text=f"Spawner",
            manager=self.ui_manager,
            object_id="#spawner_view_changer_button",
            anchors={"left": "left", "bottom": "bottom"},
        )

        pygame_gui.elements.UIButton( # ändra till en pause bild när du vet hur man gör det
            relative_rect=pygame.Rect(
                (10 + 0.66 * ORIGIN[0], -50), (0.2 * ORIGIN[0], 45)
            ),
            text=f"Pause",
            manager=self.ui_manager,
            object_id="#pause_button",
            anchors={"left": "left", "bottom": "bottom"},
        )
        
        # NOTE: Bild som visar att spelet är pausat
        # pygame_gui.elements.UIImage(
        #     relative_rect=(
        #         (15 + 0.86 * ORIGIN[0], -50), (32, 32)
        #         ),
        #     image_surface=square_image,
        #     manager=self.ui_manager,
        #     object_id="#pause_image",
        #     anchors={"left": "left", "bottom": "bottom"},
        # )

        pass

    def show_manipulate_editor(self):
        pygame_gui.elements.UISelectionList(
            relative_rect=pygame.Rect((-5, 100), (0.35 * ORIGIN[0], 142)),
            item_list=["Move", "Force", "Velocity"],
            manager=self.ui_manager,
            allow_multi_select=False,
            allow_double_clicks=False,
            object_id="#tool_selected_input",
        )
        match self.tool:
            case "move":
                pass

            case "force":
                pygame_gui.elements.UITextEntryLine(
                    relative_rect=pygame.Rect((5, 265), (0.7 * ORIGIN[0], 55)),
                    manager=self.ui_manager,
                    object_id="#force_input",
                )
                pygame_gui.elements.UITextEntryLine(
                    relative_rect=pygame.Rect((5, 355), (0.7 * ORIGIN[0], 55)),
                    manager=self.ui_manager,
                    object_id="#angle_input",
                )

            case "velocity":
                pygame_gui.elements.UITextEntryLine(
                    relative_rect=pygame.Rect((5, 265), (0.7 * ORIGIN[0], 55)),
                    manager=self.ui_manager,
                    object_id="#angle_input",
                )

                pygame_gui.elements.UITextEntryLine(
                    relative_rect=pygame.Rect((5, 355), (0.7 * ORIGIN[0], 55)),
                    manager=self.ui_manager,
                    object_id="#velocity_input",
                )

        pass

    def show_spawn_editor(self):
        # Möjligt att lägga till bilder av formerna som knappar eller bara bilder som ersättning eller komplement till en UISelectionList
        # pygame_gui.elements.UIImage(
        #     relative_rect=pygame.Rect((32, 320), (32, 32)),
        #     image_surface=pygame.Surface()
        # )

        pygame_gui.elements.UISelectionList(
            relative_rect=pygame.Rect((-5, 100), (0.35 * ORIGIN[0], 102)),
            item_list=["Rectangle", "Circle"],
            manager=self.ui_manager,
            allow_multi_select=False,
            allow_double_clicks=False,
            object_id="#shape_input",
        )

        # Gör ett sätt att välja färg, men helst med bilder av färgen istället för bara text. inte nödvändigt men coolt. Byt kanske till drop down väljare.
        """
        pygame_gui.elements.UISelectionList(
            relative_rect=pygame.Rect((-5, 350), (0.35 * ORIGIN[0], 142)),
            item_list= ["Red", "Green", "Blue"], #fler färger senare
            manager=self.ui_manager,
            allow_multi_select=False,
            allow_double_clicks=False,
            object_id="#color_input",
        )

        pygame_gui.elements.UISelectionList(
            relative_rect=pygame.Rect((0.35 * ORIGIN[0] - 20, 350), (0.35 * ORIGIN[0], 142)),
            item_list= ["Yellow", "Purple", "Orange"], #fler färger senare
            manager=self.ui_manager,
            allow_multi_select=False,
            allow_double_clicks=False,
            object_id="#color_input",
        )
        """
        pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(
                (0.35 * ORIGIN[0] + 5, 110), (0.35 * ORIGIN[0], 40)
            ),
            text="Clear",
            manager=self.ui_manager,
            tool_tip_text="Deletes all objects if double clicked",
            allow_double_clicks=True,
            object_id="#clear_button",
        )

        pygame_gui.elements.UITextEntryLine(
            relative_rect=pygame.Rect((0, 230), (0.35 * ORIGIN[0], 55)),
            manager=self.ui_manager,
            object_id="#x_coordinate_input",
        )

        pygame_gui.elements.UITextEntryLine(
            relative_rect=pygame.Rect((0.35 * ORIGIN[0], 230), (0.35 * ORIGIN[0], 55)),
            manager=self.ui_manager,
            object_id="#y_coordinate_input",
        )

        pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((3, 285), (0.25 * ORIGIN[0], 40)),
            text="Spawn",
            manager=self.ui_manager,
            tool_tip_text="Spawns the selected shape on the specified coordinates",
            object_id="#spawn_button",
        )

        # Kanske inte ens behövs, eftersom när man är i "spawn skärmen"
        pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(
                (10 + 0.25 * ORIGIN[0], 285), (0.35 * ORIGIN[0], 40)
            ),
            text="Mouse Spawn",
            manager=self.ui_manager,
            tool_tip_text="Spawns the selected shape when you left click somewhere on the coordinate grid",
            object_id="#mouse_spawn_button",
        )

        if self.shape == "circle":
            pygame_gui.elements.UITextEntryLine(
                relative_rect=pygame.Rect((0, 370), (0.7 * ORIGIN[0], 55)),
                manager=self.ui_manager,
                object_id="#radius_input",
            )

            pygame_gui.elements.UITextEntryLine(
                relative_rect=pygame.Rect((0, 470), (0.7 * ORIGIN[0], 55)),
                manager=self.ui_manager,
                object_id="#mass_input",
            )

        pass

    def set_caption(self, caption: str) -> None:
        pygame.display.set_caption(caption)

    def create_text(self, text: str, color: tuple, position: tuple, size: int) -> None:
        self.font.set_point_size(size)
        return self.font.render(text, True, color)

    def render_text(self, text: str, color: tuple, position: tuple, size: int) -> None:
        text_surface = self.create_text(text, color, position, size)
        self.screen.blit(text_surface, position)

    def render_objects(self, objects: list) -> None:
        for obj in objects:
            obj.render(self)

    def render_rectangle(self, rectangle):
        pygame.draw.rect(
            surface=self.screen,
            color=rectangle.color,
            rect=pygame.Rect(
                self.convert_coordinates(rectangle.position.x, rectangle.position.y),
                (
                    rectangle.width * GRID_SCALE,
                    rectangle.height * GRID_SCALE,
                ),
            ),
        )

    def render_circle(self, circle):
        pygame.draw.circle(
            surface=self.screen,
            color=circle.color,
            center=self.convert_coordinates(circle.position.x, circle.position.y),
            radius=circle.radius,
        )

    def render_polygon(self, polygon):
        pygame.draw.polygon(
            surface=self.screen,
            color=polygon.color,
            points=[
                self.convert_coordinates(point.x, point.y) for point in polygon.vertices
            ],
            width=0,
        )
