import json
from curso.models import Razao, Curso, Disciplina, Docente

def importar_dados(json_file_path):
    with open(json_file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)

    # Importando Razões
    for razao_data in data['reasons']:
        razao, created = Razao.objects.get_or_create(
            razao=razao_data['reason'],
            ordem=razao_data['order']
        )
        if created:
            print(f'Successfully created reason: {razao.razao}')

    # Importando Curso
    curso_data = data['courseDetail']
    
    diretor, created = Docente.objects.get_or_create(
        nome=curso_data['directionContact'],
        email=curso_data['directionEmail']
    )
    if created:
        print(f'Successfully created director: {diretor.nome}')

    secretario, created = Docente.objects.get_or_create(
        nome=curso_data['courseSecretariatContact'],
        email=curso_data['courseSecretariatEmail']
    )
    if created:
        print(f'Successfully created secretary: {secretario.nome}')

    curso, created = Curso.objects.get_or_create(
        nome=curso_data['courseName'],
        defaults={
            'descricao': curso_data.get('presentation', ''),
            'diretor': diretor,
            'secretario': secretario,
            'competencias': curso_data.get('competences', '')
        }
    )
    if created:
        print(f'Successfully created course: {curso.nome}')
    else:
        # Update the existing course details
        curso.descricao = curso_data.get('presentation', '')
        curso.diretor = diretor
        curso.secretario = secretario
        curso.competencias = curso_data.get('competences', '')
        curso.save()

    # Associando Razões ao Curso
    for razao_data in data['reasons']:
        razao = Razao.objects.get(razao=razao_data['reason'])
        curso.razoes.add(razao)

    # Importando Disciplinas
    for disciplina_data in data['courseFlatPlan']:
        disciplina, created = Disciplina.objects.get_or_create(
            nome=disciplina_data['curricularUnitName'],
            defaults={
                'carga_horaria': disciplina_data['hrTotalContactoInt'],
                'ano': disciplina_data['curricularYear'],
                'semestre': disciplina_data['semester'],
                'ects': disciplina_data['ects']
            }
        )
        if created:
            print(f'Successfully created discipline: {disciplina.nome}')
        else:
            # Update the existing discipline details
            disciplina.carga_horaria = disciplina_data['hrTotalContactoInt']
            disciplina.ano = disciplina_data['curricularYear']
            disciplina.semestre = disciplina_data['semester']
            disciplina.ects = disciplina_data['ects']
            disciplina.save()

        # Associando Disciplinas ao Curso
        curso.disciplinas.add(disciplina)

    print('Data import completed successfully.')
