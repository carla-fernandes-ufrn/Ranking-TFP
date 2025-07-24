from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from Usuario.models import Usuario

class Command(BaseCommand):
    help = 'Criar usuários'

    def handle(self, *args, **options):
        u1= User.objects.create_user(username='carla.fernandes', first_name='Carla', last_name='Fernandes', password='123')
        Usuario.objects.create(user=u1)

        u1= User.objects.create_user(username='fernanda.mousinho', first_name='Fernanda', last_name='Mousinho', password='123')
        Usuario.objects.create(user=u1)
        
        u1= User.objects.create_user(username='duda.medeiros', first_name='Duda', last_name='Medeiros', password='123')
        Usuario.objects.create(user=u1)
        
        u1= User.objects.create_user(username='geo.faria', first_name='Geo', last_name='Faria', password='123')
        Usuario.objects.create(user=u1)
        
        u1= User.objects.create_user(username='rita.medeiros', first_name='Rita', last_name='Medeiros', password='123')
        Usuario.objects.create(user=u1)

        u1= User.objects.create_user(username='luciana.rezende', first_name='Luciana', last_name='Rezende', password='123')
        Usuario.objects.create(user=u1)

        u1= User.objects.create_user(username='cynthia.amaral', first_name='Cynthia', last_name='Amaral', password='123')
        Usuario.objects.create(user=u1)
        
        u1= User.objects.create_user(username='barbara.barbosa', first_name='Barbara', last_name='Barbosa', password='123')
        Usuario.objects.create(user=u1)
        
        u1= User.objects.create_user(username='ana.fernandes', first_name='Ana', last_name='Fernandes', password='123')
        Usuario.objects.create(user=u1)
        
        u1= User.objects.create_user(username='katia.matsui', first_name='Kátia', last_name='Matsui', password='123')
        Usuario.objects.create(user=u1)
        
        u1= User.objects.create_user(username='dany.oliveira', first_name='Dany', last_name='Oliveira', password='123')
        Usuario.objects.create(user=u1)
        
        u1= User.objects.create_user(username='charlotte.macedo', first_name='Charlotte', last_name='Macedo', password='123')
        Usuario.objects.create(user=u1)
        
        u1= User.objects.create_user(username='bia.salem', first_name='Bia', last_name='Salem', password='123')
        Usuario.objects.create(user=u1)
        
        u1= User.objects.create_user(username='duda.saldanha', first_name='Duda', last_name='Saldanha', password='123')
        Usuario.objects.create(user=u1)
        
        u1= User.objects.create_user(username='anselia.costa', first_name='Ansélia', last_name='Costa', password='123')
        Usuario.objects.create(user=u1)
        
        u1= User.objects.create_user(username='isabele.diniz', first_name='Isabele', last_name='Diniz', password='123')
        Usuario.objects.create(user=u1)
        
        u1= User.objects.create_user(username='mahanna.sekine', first_name='Mahanna', last_name='Sekine', password='123')
        Usuario.objects.create(user=u1)
        
        u1= User.objects.create_user(username='ilza.oliveira', first_name='Ilza', last_name='Oliveira', password='123')
        Usuario.objects.create(user=u1)
        
        u1= User.objects.create_user(username='dandan.souza', first_name='Dandan', last_name='Souza', password='123')
        Usuario.objects.create(user=u1)
        
        u1= User.objects.create_user(username='patricia.lopes', first_name='Patrícia', last_name='Lopes', password='123')
        Usuario.objects.create(user=u1)
        
        u1= User.objects.create_user(username='juliana.curvelo', first_name='Juliana', last_name='Curvelo', password='123')
        Usuario.objects.create(user=u1)
        
        u1= User.objects.create_user(username='geovana.da.silva', first_name='Geovana', last_name='da Silva', password='123')
        Usuario.objects.create(user=u1)
        
        u1= User.objects.create_user(username='mariangela.lima', first_name='Mariângela', last_name='Lima', password='123')
        Usuario.objects.create(user=u1)
        
        u1= User.objects.create_user(username='karilany.coutinho', first_name='Karilany', last_name='Coutinho', password='123')
        Usuario.objects.create(user=u1)
        
        u1= User.objects.create_user(username='raquel.rocha', first_name='Raquel', last_name='Rocha', password='123')
        Usuario.objects.create(user=u1)
        
        u1= User.objects.create_user(username='claudia.araujo', first_name='Cláudia', last_name='Araújo', password='123')
        Usuario.objects.create(user=u1)
        
        u1= User.objects.create_user(username='edna.alves', first_name='Edna', last_name='Alves', password='123')
        Usuario.objects.create(user=u1)

        u1= User.objects.create_user(username='daniela.bezerra', first_name='Daniela', last_name='Bezerra', password='123')
        Usuario.objects.create(user=u1)

        u1= User.objects.create_user(username='ludmila.lopes', first_name='Ludmila', last_name='Lopes', password='123')
        Usuario.objects.create(user=u1)
        
        u1= User.objects.create_user(username='larissa.freire', first_name='Larissa', last_name='Freire', password='123')        
        Usuario.objects.create(user=u1)

        u1= User.objects.create_user(username='thay.vasconcelos', first_name='Thay', last_name='Vasconcelos', password='123')        
        Usuario.objects.create(user=u1)

        u1= User.objects.create_user(username='celi.meneses', first_name='Celi', last_name='Meneses', password='123')        
        Usuario.objects.create(user=u1)

        u1= User.objects.create_user(username='maria.antonia', first_name='Maria', last_name='Antônia', password='123')        
        Usuario.objects.create(user=u1)

        u1= User.objects.create_user(username='talita.tribst', first_name='Talita', last_name='Tribst', password='123')        
        Usuario.objects.create(user=u1)

        u1= User.objects.create_user(username='rebeca.liberato', first_name='Rebeca', last_name='Liberato', password='123')        
        Usuario.objects.create(user=u1)

        u1= User.objects.create_user(username='samara.mendonca', first_name='Samara', last_name='Mendonça', password='123')        
        Usuario.objects.create(user=u1)

        u1= User.objects.create_user(username='thais.valadao', first_name='Thais', last_name='Valadão', password='123')        
        Usuario.objects.create(user=u1)

        u1= User.objects.create_user(username='stephanie.revoredo', first_name='Stephanie', last_name='Revoredo', password='123')        
        Usuario.objects.create(user=u1)

        u1= User.objects.create_user(username='luana.faria', first_name='Luana', last_name='Faria', password='123')
        Usuario.objects.create(user=u1)

        u1= User.objects.create_user(username='suzana.campos', first_name='Suzana', last_name='Campos', password='123')
        Usuario.objects.create(user=u1)

        u1= User.objects.create_user(username='gilka.da.mata', first_name='Gilka', last_name='da Mata', password='123')
        Usuario.objects.create(user=u1)

        u1= User.objects.create_user(username='vivianne.nascimento', first_name='Vivianne', last_name='Nascimento', password='123')
        Usuario.objects.create(user=u1)

        u1= User.objects.create_user(username='denise.arouca', first_name='Denise', last_name='Arouca', password='123')
        Usuario.objects.create(user=u1)

        u1= User.objects.create_user(username='bruna.leticia', first_name='Bruna', last_name='Letícia', password='123')
        Usuario.objects.create(user=u1)

        u1= User.objects.create_user(username='suely.curvelo', first_name='Suely', last_name='Curvelo', password='123')
        Usuario.objects.create(user=u1)

        u1= User.objects.create_user(username='sara.isabela', first_name='Sara', last_name='Isabela', password='123')
        Usuario.objects.create(user=u1)

        u1= User.objects.create_user(username='hanna.gottschalck', first_name='Hanna', last_name='Gottschalck', password='123')
        Usuario.objects.create(user=u1)

        u1= User.objects.create_user(username='vanessa.lyra', first_name='Vanessa', last_name='Lyra', password='123')
        Usuario.objects.create(user=u1)

        u1= User.objects.create_user(username='dany.lima', first_name='Dany', last_name='Lima', password='123')
        Usuario.objects.create(user=u1)

        u1= User.objects.create_user(username='elba.roberta', first_name='Elba', last_name='Roberta', password='123')
        Usuario.objects.create(user=u1)

        self.stdout.write(self.style.SUCCESS('Usuários criados com sucesso!'))