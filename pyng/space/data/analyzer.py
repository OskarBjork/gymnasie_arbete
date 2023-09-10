class Analyzer:
    def check_if_any_objects_are_inside_of_each_other(self, objects):
        for obj in objects:
            for other_obj in objects:
                if obj == other_obj:
                    continue

                if obj.is_inside_of_other_object(other_obj):
                    self.resolve_collision(obj, other_obj)

    def resolve_collision(self, obj, other_obj):
        pass
