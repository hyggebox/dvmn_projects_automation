from django.db import models


class TimeSlot(models.Model):
    timeslot = models.CharField(
        verbose_name='Слот времени',
        max_length=200)

    def __str__(self):
        return f'{self.timeslot}'

    class Meta:
        verbose_name = 'Временной слот'
        verbose_name_plural = 'Временные слоты'


class PM(models.Model):
    tg_id = models.IntegerField(verbose_name='ID ПМ в телеграмме')
    name = models.CharField(
        verbose_name='Имя ПМ',
        max_length=200)
    time_slots = models.ManyToManyField(
        TimeSlot,
        verbose_name='Временной слот',
        max_length=200,
        related_name='pms'
    )

    def __str__(self):
        return f'ПМ {self.name}'

    def get_time_slots(self):
        return " | ".join([str(time_slot) for time_slot in self.time_slots.all()])

    class Meta:
        verbose_name = 'ПМа'
        verbose_name_plural = 'ПМы'


class Group(models.Model):
    pm = models.ForeignKey(
        PM,
        verbose_name='ПМ группы',
        related_name='groups',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    time_slot = models.ForeignKey(
        TimeSlot,
        verbose_name='Время группы',
        related_name='groups',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    def __str__(self):
        return f'{self.pm.name}-{self.time_slot.timeslot}'

    class Meta:
        verbose_name = 'Группу'
        verbose_name_plural = 'Группы'


class Student(models.Model):
    tg_id = models.IntegerField(verbose_name='ID ученика в телеграмме')
    f_name = models.CharField(verbose_name='Имя ученика',
                              max_length=200)
    l_name = models.CharField(verbose_name='Фамилия ученика',
                              null=True,
                              blank=True,
                              max_length=200)
    level = models.CharField(verbose_name='Уровень ученика',
                             max_length=200)
    best_time_slots = models.ManyToManyField(
        TimeSlot,
        verbose_name='Наиболее подходящие слоты',
        related_name='best_time_students',
        blank=True
    )
    ok_time_slots = models.ManyToManyField(
        TimeSlot,
        verbose_name='Допустимые слоты',
        related_name='ok_time_students',
        blank=True
    )
    group = models.ForeignKey(
        Group,
        verbose_name='Группа',
        related_name='students',
        on_delete=models.SET_NULL,
        blank=True,
        null=True
    )
    link_sent = models.BooleanField(default=False)

    def __str__(self):
        return f'Ученик {self.f_name}'

    def get_best_time_slots(self):
        return " | ".join(
            [str(time_slot) for time_slot in self.best_time_slots.all()])

    def get_ok_time_slots(self):
        return " | ".join(
            [str(time_slot) for time_slot in self.ok_time_slots.all()])

    class Meta:
        verbose_name = 'Ученика'
        verbose_name_plural = 'Ученики'