# Usuario/script_criar_usuarios.py

from django.contrib.auth.models import User
from Usuario.models import Usuario

def executar_criacao():
    usuarios = [
        ("carla.fernandes", "Carla", "Fernandes"),
        ("fernanda.mousinho", "Fernanda", "Mousinho"),
        ("duda.medeiros", "Duda", "Medeiros"),
        ("geo.faria", "Geo", "Faria"),
        ("rita.medeiros", "Rita", "Medeiros"),
        ("luciana.rezende", "Luciana", "Rezende"),
        ("cynthia.amaral", "Cynthia", "Amaral"),
        ("barbara.barbosa", "Barbara", "Barbosa"),
        ("ana.fernandes", "Ana", "Fernandes"),
        ("katia.matsui", "Kátia", "Matsui"),
        ("dany.oliveira", "Dany", "Oliveira"),
        ("charlotte.macedo", "Charlotte", "Macedo"),
        ("bia.salem", "Bia", "Salem"),
        ("duda.saldanha", "Duda", "Saldanha"),
        ("anselia.costa", "Ansélia", "Costa"),
        ("isabele.diniz", "Isabele", "Diniz"),
        ("mahanna.sekine", "Mahanna", "Sekine"),
        ("ilza.oliveira", "Ilza", "Oliveira"),
        ("dandan.souza", "Dandan", "Souza"),
        ("patricia.lopes", "Patrícia", "Lopes"),
        ("juliana.curvelo", "Juliana", "Curvelo"),
        ("geovana.da.silva", "Geovana", "da Silva"),
        ("mariangela.lima", "Mariângela", "Lima"),
        ("karilany.coutinho", "Karilany", "Coutinho"),
        ("raquel.rocha", "Raquel", "Rocha"),
        ("claudia.araujo", "Cláudia", "Araújo"),
        ("edna.alves", "Edna", "Alves"),
        ("daniela.bezerra", "Daniela", "Bezerra"),
        ("ludmila.lopes", "Ludmila", "Lopes"),
        ("larissa.freire", "Larissa", "Freire"),
        ("thay.vasconcelos", "Thay", "Vasconcelos"),
        ("celi.meneses", "Celi", "Meneses"),
        ("maria.antonia", "Maria", "Antônia"),
        ("talita.tribst", "Talita", "Tribst"),
        ("rebeca.liberato", "Rebeca", "Liberato"),
        ("samara.mendonca", "Samara", "Mendonça"),
        ("thais.valadao", "Thais", "Valadão"),
        ("stephanie.revoredo", "Stephanie", "Revoredo"),
        ("luana.faria", "Luana", "Faria"),
        ("suzana.campos", "Suzana", "Campos"),
        ("gilka.da.mata", "Gilka", "da Mata"),
        ("vivianne.nascimento", "Vivianne", "Nascimento"),
        ("denise.arouca", "Denise", "Arouca"),
        ("bruna.leticia", "Bruna", "Letícia"),
        ("suely.curvelo", "Suely", "Curvelo"),
        ("sara.isabela", "Sara", "Isabela"),
        ("hanna.gottschalck", "Hanna", "Gottschalck"),
        ("vanessa.lyra", "Vanessa", "Lyra"),
        ("dany.lima", "Dany", "Lima"),
        ("elba.roberta", "Elba", "Roberta"),
    ]

    for username, first_name, last_name in usuarios:
        if not User.objects.filter(username=username).exists():
            u = User.objects.create_user(
                username=username,
                first_name=first_name,
                last_name=last_name,
                password="123"
            )
            Usuario.objects.create(user=u)
