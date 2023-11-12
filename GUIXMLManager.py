import xml.etree.ElementTree as et


class GUIXMLManager:

    def __init__(self, xml_file):
        self._path = xml_file
        self._xml_tree = et.parse(xml_file)
        self._xml_root = self._xml_tree.getroot()

    def get_value_attrib_in_tag(self, xml_tag: str, attrib: str, type_content="resource"):
        elements = self._xml_tree.find(xml_tag).findall(type_content)
        out = []
        for e in elements:
            try:
                out.append(e.attrib[attrib])
            except:
                pass
        return out

    def get_root_attrib_value(self, root_tag: str, attrib: str):
        element = self._xml_tree.find(root_tag)
        if attrib in element.attrib.keys():
            return element.attrib[attrib]
        else:
            return -1

    def delete(self, container_tag: str, tag_delete: str, attrib: str, value_attrib: str):
        container = self._xml_root.find(container_tag)
        elements = container.findall(tag_delete)
        for e in elements:
            if e.attrib[attrib] == value_attrib:
                container.remove(e)
        et.indent(self._xml_tree, space='    ')
        self._xml_tree.write(self._path)

    def insert_attrib_value(self, container_tag: str, tag_insert: str, attrib: str, new_value_attrib: str):
        container = self._xml_root.find(container_tag)
        element = container.find(tag_insert)
        element.attrib[attrib] = new_value_attrib
        et.indent(self._xml_tree, space='    ')
        self._xml_tree.write(self._path)

    def container_tag_change_attrib(self, tag_container: str, attrib: str, new_value_attib: str):
        container = self._xml_root.find(tag_container)
        container.attrib[attrib] = new_value_attib
        et.indent(self._xml_tree, space='    ')
        self._xml_tree.write(self._path)

    def add_element_in_container(self, root_tag: str, element_tag: str, attr_and_values: dict):
        container = self._xml_root.find(root_tag)
        child = et.Element(element_tag, attr_and_values)
        container.insert(1, child)
        et.indent(self._xml_tree, space='    ')
        self._xml_tree.write(self._path)

    def delete_element_in_container(self, root_tag: str, element_tag: str, attr_and_values: dict):
        container = self._xml_root.find(root_tag)
        child = container.find(element_tag, attr_and_values)
        container.remove(child)
        et.indent(self._xml_tree, space='    ')
        self._xml_tree.write(self._path)

    def get_list_elements_in_container(self, root_tag: str, element_tag: str):
        container = self._xml_root.find(root_tag)
        return container.findall(element_tag)

    def replace_attrib_value(self, root_tag: str, element_tag: str, last_attrs: dict, new_attrs: dict):
        container = self._xml_root.find(root_tag)
        child = container.find(element_tag, last_attrs)
        child.attrib.update(new_attrs)
        et.indent(self._xml_tree, space='    ')
        self._xml_tree.write(self._path)

    def replace_one_attrib_value(self, root_tag: str, element_tag: str, new_attrs: dict):
        container = self._xml_root.find(root_tag)
        child = container.find(element_tag)
        child.attrib.update(new_attrs)
        et.indent(self._xml_tree, space='    ')
        self._xml_tree.write(self._path)


if __name__ == "__main__":
    aux = {
        "name": "hola.gsd",
        "path": "sklñdfjsldkfjsldkfjsdlkf",
        "fecha": "23423423"
    }
    xml = GUIXMLManager("./config.xml")
    xml.add_element_in_container("projects", "project", aux)

    xml.replace_attrib_value("projects", "project", aux, {"fecha": "Hola jajaja"})


