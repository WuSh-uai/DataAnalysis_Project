from django.db import models

class Consumption(models.Model):
    """学生消费数据表"""
    CONSUMPTION_TYPES = [
        ('餐饮', '餐饮'),
        ('文具', '文具'),
        ('饮品', '饮品'),
        ('其他', '其他'),
    ]

    LOCATIONS = [
        ('一食堂', '一食堂'),
        ('二食堂', '二食堂'),
        ('校园超市', '校园超市'),
        ('奶茶店', '奶茶店'),
    ]

    student_id = models.CharField('学号', max_length=20, db_index=True)
    name = models.CharField('姓名', max_length=50)
    consumption_type = models.CharField('消费类型', max_length=20, choices=CONSUMPTION_TYPES)
    amount = models.DecimalField('消费金额', max_digits=10, decimal_places=2)
    consumption_time = models.DateField('消费时间', db_index=True)
    location = models.CharField('消费地点', max_length=50, choices=LOCATIONS)
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    updated_at = models.DateTimeField('更新时间', auto_now=True)

    class Meta:
        db_table = 'consumption'
        verbose_name = '消费记录'
        verbose_name_plural = '消费记录'
        ordering = ['-consumption_time']

    def __str__(self):
        return f"{self.student_id} - {self.name} - {self.consumption_type} - ¥{self.amount}"