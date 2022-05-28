
# numerator와 denominator를 instance 변수와, 그와 관련된 메서드를 갖는  클래스

class Fraction:

    # 생성자 : 인자로 받은 값으로 instance 변수 numerator와 denominator를 초기화
    def __init__(self, numerator=0, denominator=1):
        self._numerator = numerator
        self._denominator = denominator


    # 객체의 numerator 변수의 값을 바꾸기 위한 mutator 메서드
    def setNumerator(self, numerator):
        self._numerator = numerator


    # 객체의 numerator 변수에 접근해 값을 얻기 위한 accessor 메서드
    def getNumerator(self):
        return self._numerator


    def setDenominator(self, denominator):
        self._denominator = denominator


    def getDenominator(self):
        return self._denominator

    # m과 n의 최대공약수를 구하기 위한 메서드
    def GCD(self, m, n):
        while n != 0:
            t = n
            n = m % n
            m = t
        return m


    # GCD 메서드로 최대공약수를 구한 것으로, 분자와 분모를 각각 나눈다
    def reduce(self):
        GCD = self.GCD(self.getNumerator(), self.getDenominator())
        self.setNumerator(self.getNumerator() // GCD)
        self.setDenominator(self.getDenominator() // GCD)
        



def main():
    # numerator와 denominator로 사용할 값을 입력받고
    numerator = int(input("Enter numerator of fraction: "))
    denominator = int(input("Enter denominator of fraction: "))

    # 이 값들을 인자로 전달해 Fraction 객체 fraction을 생성한다
    fraction = Fraction(numerator, denominator)

    # 객체 fraction의 reduce 메서드를 호출해 최대공약수로 나눠진 값을 구한다.
    fraction.reduce()

    print("Reduction to lowest terms: {0}/{1}"
          .format(fraction.getNumerator(), fraction.getDenominator()))



main()





