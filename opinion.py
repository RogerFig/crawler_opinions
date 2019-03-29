import simplejson as json

'''
    
'''
class Opinion:
    def __init__(self, id, autor , nome_objeto, data, estrelas, texto, thumbs_up, thumbs_down, recommend='', link=''):
        self.id = id
        self.autor = autor
        self.nome_objeto = nome_objeto
        self.data = data
        self.estrelas = estrelas
        self.texto = texto
        self.thumbs_up = int(thumbs_up)
        self.thumbs_down = int(thumbs_down)
        self.recommend = recommend
        self.link = link
    
    def __repr__(self):
        return self.texto

    def __str__(self):
        return self.texto

    def to_json(self):
        return json.dumps({"id":self.id, "autor":self.autor, "objeto":self.nome_objeto, "data":self.data, 
        "estrelas":self.estrelas, "texto":self.texto, "likes":self.thumbs_up,'deslikes':self.thumbs_down, 
        "recommend":self.recommend, "link":self.link})