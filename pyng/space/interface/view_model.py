from math import ceil

import pygame
import pygame_gui
from pygame import Surface

from pyng.config import RED, BLACK, WHITE, OUTLINE_TEAL, GRID_SCALE, PIXELS_PER_METER, ORIGIN, OUTLINE_SIZE
from pyng.space.vectors import Vector2D
from pyng.space.phys_obj import Circle

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
        self.spawn_gravity_toggle_button = None
        self.info_text_box = None
        self.selected_object = None
        self.object_info_kwargs = {
            "position_x": "", 
            "position_y": "", 
            "velocity_x": "", 
            "velocity_y": "",
            "force_x": "",
            "force_y": "",
            "mass": ""
            }

    def convert_coordinates(self, x, y) -> (float, float):
        return x, self.screen.get_height() - y

    def clear(self):
        self.screen.fill(WHITE)

    def update(self, ui_refresh_rate: float):
        pygame.display.update()
        self.ui_manager.update(ui_refresh_rate)

    def update_object_info(self):
        self.object_info_kwargs["position_x"] = int(self.selected_object.position.x) - ORIGIN[0]
        self.object_info_kwargs["position_y"] = int(self.selected_object.position.y) - ORIGIN[1]

        self.object_info_kwargs["velocity_x"] = int(self.selected_object.velocity.x)
        self.object_info_kwargs["velocity_y"] = int(self.selected_object.velocity.y)
        
        self.object_info_kwargs["force_x"] = self.selected_object.force.x
        self.object_info_kwargs["force_y"] = self.selected_object.force.y

        self.object_info_kwargs["mass"] = self.selected_object.mass

        # Rebuilds the UIelement in order to display the new text 
        self.info_text_box.kill()
        self.build_info_box()


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
                    self.render_text(
                        "Teleporter Coordinates:",
                        BLACK,
                        (10, 245),
                        20,
                    )

                case "force":
                    self.render_text(
                        "Force [Newton]:",
                        BLACK,
                        (10, 245),
                        20,
                    )

                case "velocity":
                    self.render_text(
                        "Velocity x, y [m/s]:",
                        BLACK,
                        (10, 245),
                        20,
                    )

            self.render_text(
                "Object Info:",
                BLACK,
                (10, self.height - 380),
                30,           
            )

    def render_or_uptade_selected_object_related(self):
        if self.selected_object is not None: # Om ett objekt är valt
            # Rendera Outline
            if isinstance(self.selected_object, Circle):
                outline = Circle(color=OUTLINE_TEAL, position=self.selected_object.position, mass=10, radius=self.selected_object.radius+OUTLINE_SIZE)
                self.render_circle(outline)
            else:
                outline_radius = self.selected_object.aabb.min.get_distance_to(self.selected_object.aabb.max) / 2
                outline = Circle(color=OUTLINE_TEAL, mass=10, position=self.selected_object.position, radius=outline_radius+OUTLINE_SIZE)
                self.render_circle(outline)
            # Uppdatera Info Rutan
            self.update_object_info()

    def render_ui(self, ui_manager):
        self.show_grid()
        ui_manager.draw_ui(self.screen)

    def show_mode_buttons(self):
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
    
    def build_info_box(self):
        self.info_text_box = pygame_gui.elements.UITextBox(
                html_text=
                f"""
                Position: {self.object_info_kwargs["position_x"]}x, {self.object_info_kwargs["position_y"]}y
                <br>Velocity: {self.object_info_kwargs["velocity_x"]}x, {self.object_info_kwargs["velocity_y"]}y
                <br>Force: {self.object_info_kwargs["force_x"]}x, {self.object_info_kwargs["force_y"]}y
                <br>Mass: {self.object_info_kwargs["mass"]}
                """,
                relative_rect=pygame.Rect((0, -350), (0.85 * ORIGIN[0], 280)),
                manager=self.ui_manager,
                anchors={"left": "left", "bottom": "bottom"},
                object_id="#info_text_box",
            )
    
    def reset_info_box_info(self):
        for element in self.object_info_kwargs:
            self.object_info_kwargs[element] = ""

    def create_confirm_buttons(self, height):
        pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((8, height), (0.2 * ORIGIN[0], 45)),
            text="Set",
            tool_tip_text="Press to set the values specified above to the selected object",
            object_id="#set_button"
        )
        pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((8 + 0.2 * ORIGIN[0], height), (0.2 * ORIGIN[0], 45)),
            text="Add",
            tool_tip_text="Press to add the specified values to the selected objects current values",
            object_id="#add_button"
        )       

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
                pygame_gui.elements.UITextEntryLine(
                    relative_rect=pygame.Rect((5, 265), (0.3 * ORIGIN[0], 55)),
                    manager=self.ui_manager,
                    object_id="#x_teleport_input",
                    placeholder_text="x"
                )
                pygame_gui.elements.UITextEntryLine(
                    relative_rect=pygame.Rect((0.3 * ORIGIN[0], 265), (0.3 * ORIGIN[0], 55)),
                    manager=self.ui_manager,
                    object_id="#y_teleport_input",
                    placeholder_text="y"
                )
                pygame_gui.elements.UIButton(
                    relative_rect=pygame.Rect((8, 320), (0.35 * ORIGIN[0], 45)),
                    text="Teleport",
                    tool_tip_text="Teleport selected object to your coordinates",
                    object_id="#teleport_button"
                )
                pass
                

            case "force":
                pygame_gui.elements.UITextEntryLine(
                    relative_rect=pygame.Rect((5, 265), (0.3 * ORIGIN[0], 55)),
                    manager=self.ui_manager,
                    object_id="#x_force_input",
                    placeholder_text="x"
                )
                pygame_gui.elements.UITextEntryLine(
                    relative_rect=pygame.Rect((0.3 * ORIGIN[0], 265), (0.3 * ORIGIN[0], 55)),
                    manager=self.ui_manager,
                    object_id="#y_force_input",
                    placeholder_text="y"
                )
                self.create_confirm_buttons(320)

            case "velocity":
                pygame_gui.elements.UITextEntryLine(
                    relative_rect=pygame.Rect((5, 265), (0.3 * ORIGIN[0], 55)),
                    manager=self.ui_manager,
                    object_id="#x_velocity_input",
                    placeholder_text="x"
                )

                pygame_gui.elements.UITextEntryLine(
                    relative_rect=pygame.Rect((0.3 * ORIGIN[0], 265), (0.3 * ORIGIN[0], 55)),
                    manager=self.ui_manager,
                    object_id="#y_velocity_input",
                    placeholder_text="y"
                )
                self.create_confirm_buttons(320)

        if True: #self.selected_object is not None: #Om ett objekt är valt
            self.build_info_box()
        
        pass

    def show_spawn_editor(self, spawn_gravity=False):
        # unselects object
        if not self.selected_object == None:
            self.selected_object = None
            self.reset_info_box_info()
        
        # Möjligt att lägga till bilder av formerna som knappar eller bara bilder som ersättning eller komplement till en UISelectionList
        # pygame_gui.elements.UIImage(
        #     relative_rect=pygame.Rect((32, 320), (32, 32)),
        #     image_surface=pygame.Surface()
        # )

        pygame_gui.elements.UISelectionList(
            relative_rect=pygame.Rect((-5, 100), (0.35 * ORIGIN[0], 102)),
            item_list=["Rectangle", "Circle", "Polygon"],
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

        self.spawn_gravity_toggle_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(
                (10 + 0.25 * ORIGIN[0], 285), (0.37 * ORIGIN[0], 40)
            ),
            text="Gravity: Off",
            manager=self.ui_manager,
            tool_tip_text="Spawned objects will have gravity if On",
            object_id="#spawn_gravity_toggle_button",
        )
        
        if spawn_gravity: # Ser till så att knappen inte visar felaktig information när den skapas på nytt
            self.spawn_gravity_toggle_button.set_text("Gravity: On")


        match self.shape:
            case "circle":
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
            case "rectangle":
                pygame_gui.elements.UITextEntryLine(
                    relative_rect=pygame.Rect((0, 370), (0.7 * ORIGIN[0], 55)),
                    manager=self.ui_manager,
                    object_id="#width_input",
                )
                
                pygame_gui.elements.UITextEntryLine(
                    relative_rect=pygame.Rect((0, 470), (0.7 * ORIGIN[0], 55)),
                    manager=self.ui_manager,
                    object_id="#height_input",
                )

            case "polygon":
                pygame_gui.elements.UITextEntryLine(
                    relative_rect=pygame.Rect((0, 370), (0.7 * ORIGIN[0], 55)),
                    manager=self.ui_manager,
                    object_id="#side_length_input",
                )
                
                pygame_gui.elements.UITextEntryLine(
                    relative_rect=pygame.Rect((0, 470), (0.7 * ORIGIN[0], 55)),
                    manager=self.ui_manager,
                    object_id="#num_of_sides_input",
                )
                
                pygame_gui.elements.UITextEntryLine(
                    relative_rect=pygame.Rect((0, 570), (0.7 * ORIGIN[0], 55)),
                    manager=self.ui_manager,
                    object_id="#mass_input",
                )


    def set_caption(self, caption: str) -> None:
        pygame.display.set_caption(caption)

    def create_text(self, text: str, color: tuple, position: tuple, size: int) -> None:
        self.font.set_point_size(size)
        return self.font.render(text, True, color)

    def render_text(self, text: str, color: tuple, position: tuple, size: int) -> None:
        text_surface = self.create_text(text, color, position, size)
        self.screen.blit(text_surface, position)

    def render_lable(self, text: str, position: tuple = (0, 0), size: int = 10, anchors: dict = {"left": "left", "top": "top"}, id: str = None):
        # NOTE: UILabels SUGER! JAG HATAR DEM! JAG SPENDERADE ALLDELES FÖR MYCKET TID PÅ ATT FÅ DETHÄR SKRÄPET ATT FUNKA MEN DE ÄR SÅ DÅLIGT ATT DET INTE ENS GÅR. Trash >:(
        pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect(position, (200, 300)),
            text=text,
            manager=self.ui_manager,
            object_id=id,
            anchors=anchors
        )

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
