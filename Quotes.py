class Quotes:

    __quotes = [
	"Vim, vi, venci",
	"É melhor sofrer o pior agora do que viver no eterno medo dele.",
    "Não há glória maior que perdoar a quem me atacou, e premiar a quem me serviu.",
    "Há nos confins da Ibéria um povo que nem se governa nem se deixa governar.",
    "A sorte está lançada.",
    "Nada existe de tão difícil que não seja vencível.",
    "Acreditamos com facilidade no que desejamos.",
    "Vale mais romper de uma vez do que alimentar permanente suspeita.",
    "Os covardes morrem muito antes de sua verdadeira morte.",
    "Todos os maus precedentes começam com medidas perfeitamente justificáveis.",
    "Normalmente os homens preocupam-se mais com aquilo que não podem ver que com aquilo que podem.",
    "O costume é o mestre de todas as coisas.",
    "É preferível ser o primeiro numa aldeia a ser o segundo em Roma.",
    "A mulher é feia ou bela, conforme os olhos que a vêem.",
    "O que está fora da vista perturba mais a mente dos homens do que aquilo que pode ser visto.",
    "Eu não prefiro nada além deles agindo como eles mesmos, e eu gosto de mim mesmo.",
    "A fortuna(destino ou sina), em poucos instantes, produz grandes mudanças.",
    "Cada qual é artífice da própria sorte."
    ]

    def quote(self):

        import random
        return random.choice(self.__quotes)

