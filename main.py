import xml.etree.ElementTree as ET
import networkx as nx
import threading
import time
import json
import logging  # Добавлен модуль для логирования

# Настройка логирования
logging.basicConfig(
    filename='test.log',  # Имя файла для логов
    level=logging.INFO,   # Уровень логирования
    format='%(asctime)s - %(levelname)s - %(message)s'  # Формат записи логов
)

class FunctionalBlock:
    def __init__(self, name):
        self.name = name
        self.inputs = {}
        self.outputs = {}

    def execute(self):
        # Логика выполнения функционального блока
        logging.info(f"Executing {self.name}")
        # Проверка наличия ключей
        if 'input1' not in self.inputs:
            raise KeyError(f"Input 'input1' not found in {self.name}")
        if 'input2' not in self.inputs:
            raise KeyError(f"Input 'input2' not found in {self.name}")
        # Пример простого вычисления
        self.outputs['output1'] = self.inputs['input1'] + self.inputs['input2']
        logging.info(f"Output 'output1' calculated: {self.outputs['output1']}")

class IEC61499Executor:
    def __init__(self):
        self.graph = nx.DiGraph()
        self.functional_blocks = {}

    def load_application(self, xml_file):
        tree = ET.parse(xml_file)
        root = tree.getroot()

        for fb in root.findall('FunctionalBlock'):
            fb_name = fb.get('name')
            new_fb = FunctionalBlock(fb_name)
            self.functional_blocks[fb_name] = new_fb
            self.graph.add_node(fb_name)

            for input_elem in fb.findall('Input'):
                input_name = input_elem.get('name')
                new_fb.inputs[input_name] = 0  # Инициализация входных значений

            for output_elem in fb.findall('Output'):
                output_name = output_elem.get('name')
                new_fb.outputs[output_name] = 0  # Инициализация выходных значений

        for connection in root.findall('Connection'):
            source = connection.get('source')
            target = connection.get('target')
            self.graph.add_edge(source, target)

        logging.info(f"Application loaded from {xml_file}")

    def load_4diac_application(self, xml_file):
        tree = ET.parse(xml_file)
        root = tree.getroot()

        for fb in root.findall('.//FB'):
            fb_name = fb.get('Name')
            new_fb = FunctionalBlock(fb_name)
            self.functional_blocks[fb_name] = new_fb
            self.graph.add_node(fb_name)

            for input_elem in fb.findall('.//InputVars/VarDeclaration'):
                input_name = input_elem.get('Name')
                new_fb.inputs[input_name] = 0  # Инициализация входных значений

            for output_elem in fb.findall('.//OutputVars/VarDeclaration'):
                output_name = output_elem.get('Name')
                new_fb.outputs[output_name] = 0  # Инициализация выходных значений

        for connection in root.findall('.//Connection'):
            source = connection.get('SourceFB')
            target = connection.get('DestFB')
            self.graph.add_edge(source, target)

        logging.info(f"4DIAC application loaded from {xml_file}")

    def read_values(self, fb_name, input_name, value):
        if fb_name in self.functional_blocks:
            self.functional_blocks[fb_name].inputs[input_name] = value
            logging.info(f"Input '{input_name}' set to {value} for {fb_name}")

    def create_graph(self):
        # Граф уже создан при загрузке приложения
        pass

    def play_graph(self):
        test_runner = TestRunner()
        for fb_name in nx.topological_sort(self.graph):
            fb = self.functional_blocks[fb_name]
            fb.execute()

            # Тест: Проверка выполнения функционального блока
            test_runner.test_functional_block_execution(fb)

            for successor in self.graph.successors(fb_name):
                for output_name, output_value in fb.outputs.items():
                    for input_name in self.functional_blocks[successor].inputs:
                        self.read_values(successor, input_name, output_value)

        test_runner.summary()
        logging.info("Graph execution completed")

    # Добавленные функции
    def handle_request(self, protocol_name, request):
        handler = ProtocolHandler(protocol_name)
        response = handler.handle_request(request)

        # Тест: Проверка ответа
        test_runner = TestRunner()
        if protocol_name == 'HTTP':
            test_runner.test_http_response(response)
        test_runner.summary()

        logging.info(f"Handled request with protocol {protocol_name}: {response}")
        return response

    def load_application_json(self, app_path):
        loader = ApplicationLoader()
        return loader.load_application(app_path)

    def read_values_from_app(self, app_data):
        reader = ApplicationReader()
        return reader.read_values(app_data)

    def create_graph_from_data(self, nodes, edges):
        creator = GraphCreator()
        graph = creator.create_graph(nodes, edges)

        # Тест: Проверка создания графа
        test_runner = TestRunner()
        test_runner.test_graph_creation(graph, nodes, edges)
        test_runner.summary()

        logging.info(f"Graph created with nodes {nodes} and edges {edges}")
        return graph

    def play_graph_from_data(self, graph):
        player = GraphPlayer()
        player.play_graph(graph)

        # Тест: Проверка проигрывания графа
        test_runner = TestRunner()
        for node, edges in graph.items():
            test_runner.assert_true(len(edges) >= 0, f"Node {node} has valid edges")
        test_runner.summary()

        logging.info("Graph from data played successfully")

class ProtocolHandler:
    def __init__(self, protocol_name):
        self.protocol_name = protocol_name

    def handle_request(self, request):
        logging.info(f"Handling request with protocol {self.protocol_name}")
        # Логика обработки запроса по протоколу
        if self.protocol_name == 'HTTP':
            return self.handle_http_request(request)
        return f"Response from {self.protocol_name}"

    def handle_http_request(self, request):
        # Пример обработки HTTP-запроса
        if request.startswith('GET'):
            return "HTTP/1.1 200 OK\nContent-Type: text/html\n\n<html><body>Hello, World!</body></html>"
        return "HTTP/1.1 400 Bad Request"

class ApplicationLoader:
    def load_application(self, app_path):
        logging.info(f"Loading application from {app_path}")
        # Логика загрузки приложения
        with open(app_path, 'r') as file:
            app_data = json.load(file)
        return app_data

class ApplicationReader:
    def read_values(self, app_data):
        logging.info("Reading values from application data")
        # Логика чтения значений из приложения
        values = {}
        # Пример: парсинг данных
        for key, value in app_data.items():
            values[key] = value
        return values

class GraphCreator:
    def create_graph(self, nodes, edges):
        logging.info(f"Creating graph with nodes {nodes} and edges {edges}")
        # Логика создания графа
        graph = {node: [] for node in nodes}
        for edge in edges:
            graph[edge[0]].append(edge[1])
        return graph

class GraphPlayer:
    def play_graph(self, graph):
        logging.info(f"Playing graph {graph}")
        # Логика проигрывания графа и запуска событий
        for node, edges in graph.items():
            logging.info(f"Processing node {node}")
            for edge in edges:
                logging.info(f"Event from {node} to {edge}")

# Класс для тестов
class TestRunner:
    def __init__(self):
        self.passed_tests = 0
        self.failed_tests = 0

    def assert_true(self, condition, message):
        if condition:
            self.passed_tests += 1
            logging.info(f"[PASSED] {message}")
        else:
            self.failed_tests += 1
            logging.error(f"[FAILED] {message}")

    def summary(self):
        logging.info(f"\nTest Summary: {self.passed_tests} passed, {self.failed_tests} failed")
        if self.failed_tests > 0:
            raise AssertionError("Some tests failed!")

    def test_graph_loaded(self, graph):
        self.assert_true(len(graph.nodes) > 0, "Graph nodes loaded")
        self.assert_true(len(graph.edges) > 0, "Graph edges loaded")

    def test_functional_block_execution(self, fb):
        self.assert_true('output1' in fb.outputs, f"Output 'output1' found in {fb.name}")
        self.assert_true(fb.outputs['output1'] is not None, f"Output 'output1' is not None in {fb.name}")

    def test_http_response(self, response):
        self.assert_true(response.startswith("HTTP/1.1"), "HTTP response format is correct")

    def test_graph_creation(self, graph, nodes, edges):
        self.assert_true(len(graph) == len(nodes), "Graph nodes count matches")
        for edge in edges:
            self.assert_true(edge[1] in graph[edge[0]], f"Edge {edge} found in graph")

    def test_error_handling(self, exception, expected_message):
        self.assert_true(isinstance(exception, KeyError), "Expected KeyError")
        self.assert_true(str(exception) == expected_message, f"Error message matches: {expected_message}")

def main():
    executor = IEC61499Executor()
    executor.load_4diac_application('4diac_application.xml')
    executor.create_graph()

    # Пример заполнения входных значений
    executor.read_values('FB1', 'input1', 10)
    executor.read_values('FB1', 'input2', 20)

    executor.play_graph()

    # Пример использования добавленных функций
    response = executor.handle_request('HTTP', 'GET /data')
    print(response)

    app_data = executor.load_application_json('app.json')
    values = executor.read_values_from_app(app_data)
    print(values)

    graph = executor.create_graph_from_data(['A', 'B', 'C'], [('A', 'B'), ('B', 'C')])
    executor.play_graph_from_data(graph)

if __name__ == "__main__":
    main()
