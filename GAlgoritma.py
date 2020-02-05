import numpy

def fitness_hesap(esitlik_girisler, pop):
    #fitness hesap kitap...
    fitness = numpy.sum(pop*esitlik_girisler, axis=1)
    return fitness

def ebeveyn_secimi(pop, fitness, ebeveyn_sayisi):
    # Yeni nesil için ebeveyn seçimi...
    ebeveynler = numpy.empty((ebeveyn_sayisi, pop.shape[1]))
    for eb_sayi in range(ebeveyn_sayisi):
        max_fitness_idx = numpy.where(fitness == numpy.max(fitness))
        max_fitness_idx = max_fitness_idx[0][0]
        ebeveynler[eb_sayi, :] = pop[max_fitness_idx, :]
        fitness[max_fitness_idx] = -99999999999
    return ebeveynler

def caprazlama(ebeveynler, cocuk_boyutu):
    cocuk = numpy.empty(cocuk_boyutu)
    # Çaprazlama hangi noktadan önce ve sonra dikkate alınarak yapılacak? (Tam anlatamadım sanki ama neyse...)
    caprazlama_noktasi = numpy.uint8(cocuk_boyutu[1]/2)

    for k in range(cocuk_boyutu[0]):
        # İlk ebeveyn
        ebeveyn1_indeks = k%ebeveynler.shape[0]
        # İkinci ebeveyn
        ebeveyn2_indeks = (k+1)%ebeveynler.shape[0]
        # söz
        # isteme
        # nişan
        # düğün
        # Çocuğun yarısı ilk ebeveynden
        cocuk[k, 0:caprazlama_noktasi] = ebeveynler[ebeveyn1_indeks, 0:caprazlama_noktasi]
        # ...geriye kalan yarısı ikinci ebeveynden
        cocuk[k, caprazlama_noktasi:] = ebeveynler[ebeveyn2_indeks, caprazlama_noktasi:]
    return cocuk

def mutasyon(cocuk_caprazlama):
    # Rastgele gen değiştir...
    for gen_indeks in range(cocuk_caprazlama.shape[0]):
        rastgele_sayiyim_ben = numpy.random.uniform(-1.0, 1.0, 1)
        cocuk_caprazlama[gen_indeks, 4] = cocuk_caprazlama[gen_indeks, 4] + rastgele_sayiyim_ben
    return cocuk_caprazlama

"""
Maksimize y = w1x1+w2x2+w3x3+w4x4+w5x5+6wx6
    (x1,x2,x3,x4,x5,x6)=(4,-2,3.5,5,-11,-4.7)
    w1-w6 için en iyi değerler nelerdir lan?
"""

# Eşitlik girişleri...
esitlik_girisler = [4,-2,3.5,5,-11,-4.7]

# Değişken sayısı
degisken_sayi = 6

"""
GA parametreleri; 
    eşleştirme-çaprazlama büyüklüğü
    popülasyon büyüklüğü
"""
sol_per_pop = 8
ebeveyn_sayisi_mating = 4

# Popülasyon sayısı tanımlama
pop_size = (sol_per_pop,degisken_sayi) # The population will have sol_per_pop chromosome where each chromosome has degisken_sayi genes.
# İlk popülasyon oluştur yavrum...
yeni_populasyon = numpy.random.uniform(low=-4.0, high=4.0, size=pop_size)
print(yeni_populasyon)

nesil_sayisi = 5
for nesil in range(nesil_sayisi):
    print("Nesil : ", nesil)
    # Measing the fitness of each chromosome in the population.
    fitness = fitness_hesap(esitlik_girisler, yeni_populasyon)

    # Selecting the best ebeveynler in the population for mating.
    ebeveynler = ebeveyn_secimi(yeni_populasyon, fitness, 
                                      ebeveyn_sayisi_mating)

    # Çaprazlama
    cocuk_caprazlama = caprazlama(ebeveynler,
                                       cocuk_boyutu=(pop_size[0]-ebeveynler.shape[0], degisken_sayi))

    # Mutasyon
    cocuk_mutasyon = mutasyon(cocuk_caprazlama)

    # Ebeynler ve çocuklarla birlikte yeni popülasyon
    yeni_populasyon[0:ebeveynler.shape[0], :] = ebeveynler
    yeni_populasyon[ebeveynler.shape[0]:, :] = cocuk_mutasyon

    # Yerel-lokal en iyi
    print("En iyi yerel sonuç: ", numpy.max(numpy.sum(yeni_populasyon*esitlik_girisler, axis=1)))

# SONUÇLAR
fitness = fitness_hesap(esitlik_girisler, yeni_populasyon)

en_iyinin_indeksi = numpy.where(fitness == numpy.max(fitness))

print("En iyi küresel sonuç: ", yeni_populasyon[en_iyinin_indeksi, :])
print("En iyi küresel sonuç fitness: ", fitness[en_iyinin_indeksi])