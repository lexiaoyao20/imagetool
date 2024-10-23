from imagetool import generate_new_name


def test_generate_new_name():
    old_name = "test_image"
    prefix = "prefix"
    new_name = generate_new_name(old_name, prefix)
    assert new_name.startswith(f"{prefix}_{old_name}_")
    assert len(new_name) == len(old_name) + len(prefix) + 5  # 5 for "_" and 3 random chars


def test_generate_new_name_without_prefix():
    old_name = "test_image"
    new_name = generate_new_name(old_name, None)
    assert new_name.startswith(f"{old_name}_")
    assert len(new_name) == len(old_name) + 4  # 4 for "_" and 3 random chars
