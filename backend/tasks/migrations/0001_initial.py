# Generated by Django 4.0.5 on 2022-12-21 07:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('projects', '0002_remove_project_images_project_image'),
    ]

    operations = [
        migrations.CreateModel(
            name='TestTask',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=100, verbose_name='名称')),
                ('describe', models.TextField(default='', null=True, verbose_name='描述')),
                ('status', models.IntegerField(default=0, verbose_name='状态')),
                ('is_delete', models.BooleanField(default=False, verbose_name='删除')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='创建时间')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='projects.project')),
            ],
        ),
        migrations.CreateModel(
            name='TestResult',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=100, verbose_name='名称')),
                ('passed', models.IntegerField(default=0, verbose_name='通过用例')),
                ('error', models.IntegerField(default=0, verbose_name='错误用例')),
                ('failure', models.IntegerField(default=0, verbose_name='失败用例')),
                ('skipped', models.IntegerField(default=0, verbose_name='跳过用例')),
                ('tests', models.IntegerField(default=0, verbose_name='总用例数')),
                ('run_time', models.FloatField(default=0, verbose_name='运行时长')),
                ('result', models.TextField(default='', verbose_name='详细')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('task', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tasks.testtask')),
            ],
            options={
                'ordering': ['-create_time'],
            },
        ),
        migrations.CreateModel(
            name='TaskCaseRelevance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('case', models.TextField(default='', null=True, verbose_name='关联用例')),
                ('case_list', models.TextField(default='', null=True, verbose_name='用例列表')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('task', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tasks.testtask')),
            ],
        ),
    ]
