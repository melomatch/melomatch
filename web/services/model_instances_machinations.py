def get_unique_model_instances[T](instances_list: list[T], unique_field: str) -> list[T]:
    unique_instances = {}
    for instance in instances_list:
        unique_instances[getattr(instance, unique_field)] = instance

    return list(unique_instances.values())


def get_saved_instances_by_unsaved_and_unique_saved[T](
    saved_instances: list[T], unsaved_instances: list[T], unique_field: str
) -> list[T]:
    saved_instances_by_unique_field = {}
    for instance in saved_instances:
        saved_instances_by_unique_field[getattr(instance, unique_field)] = instance

    saved_instances = []
    for instance in unsaved_instances:
        saved_instances.append(saved_instances_by_unique_field[getattr(instance, unique_field)])
    return saved_instances
