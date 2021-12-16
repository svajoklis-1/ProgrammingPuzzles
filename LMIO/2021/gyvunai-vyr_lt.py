import argparse

parser = argparse.ArgumentParser()
parser.add_argument('in_file')
args = parser.parse_args()


class Laikas:
	def __init__(self, val, min):
		self.val = val
		self.min = min


	def paros_laikas(self):
		return self.val * 60 + self.min


	def __str__(self):
		return f'{self.val}:{self.min}'


class LaikoRezis:
	def __init__(self, pradzia, pabaiga):
		self.pradzia = pradzia
		self.pabaiga = pabaiga


	def perdengti(self, rezis):
		if rezis.pradzia.paros_laikas() > self.pradzia.paros_laikas():
			self.pradzia = rezis.pradzia

		if rezis.pabaiga.paros_laikas() < self.pabaiga.paros_laikas():
			self.pabaiga = rezis.pabaiga


	def __str__(self):
		return f'{self.pradzia} - {self.pabaiga}'


class Tvarkarastis:
	def __init__(self):
		self.reziai = []

	def prideti_rezi(self, rezis):



if __name__ == '__main__':
	para = LaikoRezis(Laikas(0, 0), Laikas(23, 59))

	in_file = open(args.in_file, 'r')

	eiluciu = int(in_file.readline())

	for i in range(eiluciu):
		laikai = in_file.readline().split(' ')
		laikai = [int(l) for l in laikai]
		gyvuno_rezis = LaikoRezis(Laikas(laikai[0], laikai[1]), Laikas(laikai[2], laikai[3]))
		print(gyvuno_rezis)

		para.perdengti(gyvuno_rezis)


	print(para)