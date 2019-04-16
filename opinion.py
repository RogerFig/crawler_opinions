import simplejson as json

'''
    
'''
class Opinion:
    def __init__(self, id, autor , nome_objeto, data, estrelas, texto, thumbs_up, thumbs_down, recommend='', link='', 
        link_perfil_user='', collect_date='', see='', wsee='', favorite='', replies=''):

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
        self.link_perfil_user = link_perfil_user
        self.collect_date = collect_date
        self.see = see
        self.wsee = wsee
        self.favorite = favorite
        self.replies = replies

    
    def __repr__(self):
        return self.texto

    def __str__(self):
        return self.texto

    def to_json(self):
        return json.dumps({"id":self.id, "autor":self.autor, "objeto":self.nome_objeto, "data":self.data, 
        "estrelas":self.estrelas, "texto":self.texto, "likes":self.thumbs_up,'unlikes':self.thumbs_down, 
        "recommend":self.recommend, "link":self.link, "link_perfil_user":self.link_perfil_user, 
        "collect_date":self.collect_date, "see":self.see, "want_see":self.wsee ,"favorite":self.favorite, "replies":self.replies})