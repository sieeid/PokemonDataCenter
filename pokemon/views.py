from django.shortcuts import render
from django.http import HttpResponse

import urllib
import json


def index(request):
    """
    포켓몬 데이터를 전송
    :param request:
    :return:
    """
    request_data = request.GET.dict()
    if 'pokemon' in request_data:
        pokemon_no = request_data['pokemon']
    else:
        pokemon_no = 0

    HttpResponse()['content_type'] = 'application/json; charset=utf-8'
    url = 'https://docs.google.com/spreadsheets/d/e/2PACX-1vRm_Lc0uln_go1zCm1kqSZ6NU2lWZzFwbVUYrda6HVE6W5r62MjDhTCTa4PkDQ6s7PP0BME01jbE23s/pub?output=csv'
    pokemon_data = urllib.request.urlopen(url).read().decode('utf-8').split('\r\n')
    result = get_pokemon(pokemon_data, int(pokemon_no))

    return HttpResponse(json.dumps(result, ensure_ascii=False), content_type="application/json")


def get_pokemon(pokemon_data, pokemon_no):
    """
    포켓몬 데이터를 사전형으로 렌더링
    :param pokemon_data:
    :param pokemon_no:
    :return:
    """
    columns = []

    for tag in pokemon_data[0].split(','):
        columns.append(tag)

    pokemon = []

    for poke_no, row in enumerate(pokemon_data):
        if poke_no == 0:
            continue
        single = {'no': poke_no}
        monster = row.split(',')

        if 0 < pokemon_no < 152 and pokemon_no == poke_no:
            for monsterData in range(len(columns)):
                single[columns[monsterData]] = monster[monsterData]
            pokemon.append(single)
        elif 0 >= pokemon_no or pokemon_no >= 152:
            for monsterData in range(len(columns)):
                single[columns[monsterData]] = monster[monsterData]
            pokemon.append(single)

    return {'result': pokemon}


def test(request):
    """
    AJAX 테스트 페이지
    :param request:
    :return:
    """

    return render(request, 'main/index.html')
