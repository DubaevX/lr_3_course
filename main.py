import json

class ProtocolHandler:
    def __init__(self, protocol_name):
        self.protocol_name = protocol_name

    def handle_request(self, request):
        print(f"Handling request with protocol {self.protocol_name}")
        # Логика обработки запроса по протоколу
        return f"Response from {self.protocol_name}"

class ApplicationLoader:
    def load_application(self, app_path):
        print(f"Loading application from {app_path}")
        # Логика загрузки приложения
        with open(app_path, 'r') as file:
            app_data = json.load(file)
        return app_data

class ApplicationReader:
    def read_values(self, app_data):
        print(f"Reading values from application data")
        # Логика чтения значений из приложения
        values = {}
        # Пример: парсинг данных
        for key, value in app_data.items():
            values[key] = value
        return values

class GraphCreator:
    def create_graph(self, nodes, edges):
        print(f"Creating graph with nodes {nodes} and edges {edges}")
        # Логика создания графа
        graph = {node: [] for node in nodes}
        for edge in edges:
            graph[edge[0]].append(edge[1])
        return graph

class GraphPlayer:
    def play_graph(self, graph):
        print(f"Playing graph {graph}")
        # Логика проигрывания графа и запуска событий
        for node, edges in graph.items():
            print(f"Processing node {node}")
            for edge in edges:
                print(f"Event from {node} to {edge}")

# # Пример файла приложения
# app_file = "app.json"
# app_data = {
#     "nodes": ["node1", "node2"],
#     "edges": [["node1", "node2"]],
#     "values": {
#         "node1": "value1",
#         "node2": "value2"
#     }
# }
# with open(app_file, 'w') as file:
#     json.dump(app_data, file)
#
# # Реализация протокола
# protocol_handler = ProtocolHandler("TCP")
# response = protocol_handler.handle_request("GET /data")
# print(response)
#
# # Загрузка приложения
# app_loader = ApplicationLoader()
# app_data = app_loader.load_application(app_file)
#
# # Чтение значений приложения
# app_reader = ApplicationReader()
# values = app_reader.read_values(app_data["values"])
# print(values)
#
# # Создание графа
# nodes = app_data["nodes"]
# edges = app_data["edges"]
# graph_creator = GraphCreator()
# graph = graph_creator.create_graph(nodes, edges)
#
# # Проигрывание графа
# graph_player = GraphPlayer()
# graph_player.play_graph(graph)
