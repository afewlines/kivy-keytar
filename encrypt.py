
class Encryptor():
    def __init__(self):
        self.alphabet = [lt for lt in "abcdefghijklmnopqrswxyz1234567890'."]

    def key_gen(self, seed):
        temp = self.alphabet[(seed % (len(self.alphabet) - 1)):] + \
            self.alphabet[:(seed % (len(self.alphabet) - 1))]
        temp.reverse()
        return temp

    def encrypt(self, target):
        letters = [c for c in target]

        out = [l for l in letters]

        key = self.key_gen(len(letters))

        for upper in range(len(self.alphabet)):
            for lower in range(len(letters)):
                if letters[lower] == self.alphabet[upper]:
                    out[lower] = key[upper]
                    pass

        return ''.join(out)

    def decrypt(self, target):
        letters = [c for c in target]

        out = [l for l in letters]

        key = self.key_gen(len(letters))

        for upper in range(len(self.alphabet)):
            for lower in range(len(letters)):
                if letters[lower] == key[upper]:
                    out[lower] = self.alphabet[upper]

        return ''.join(out)

    def file_encrypt(self, target, modify=False):
        t_file = open(target, 'r')
        final = []
        for line in t_file.readlines():
            letters = [c for c in line]

            out = [l for l in letters]

            key = self.key_gen(len(letters))

            for upper in range(len(self.alphabet)):
                for lower in range(len(letters)):
                    if letters[lower] == self.alphabet[upper]:
                        out[lower] = key[upper]

            final.append(''.join(out))

        t_file.close()

        if modify:
            t_file = open(target, 'w')
            t_file.writelines(final)
            t_file.close()

        return final

    def file_decrypt(self, target, modify=False):
        t_file = open(target, 'r')
        final = []
        for line in t_file.readlines():
            letters = [c for c in line]

            out = [l for l in letters]

            key = self.key_gen(len(letters))

            for upper in range(len(self.alphabet)):
                for lower in range(len(letters)):
                    if letters[lower] == key[upper]:
                        out[lower] = self.alphabet[upper]

            final.append(''.join(out).strip())

        t_file.close()

        if modify:
            t_file = open(target, 'w')
            t_file.writelines(final)
            t_file.close()

        return final
