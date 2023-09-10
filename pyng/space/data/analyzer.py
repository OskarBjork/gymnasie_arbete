class Analyzer:
    def check_if_any_objects_are_inside_of_each_other(self, objects):
        for obj in objects:
            for other_obj in objects:
                if obj != other_obj:
                    if obj.is_inside_of(other_obj):
                        obj.stop = True
                        other_obj.stop = True
