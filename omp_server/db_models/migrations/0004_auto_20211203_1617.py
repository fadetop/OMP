# Generated by Django 3.1.4 on 2021-12-03 16:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('db_models', '0003_host_init_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='maininstallhistory',
            name='install_status',
            field=models.IntegerField(choices=[(0, '待安装'), (1, '安装中'), (2, '安装成功'), (3, '安装失败'), (4, '正在注册')], default=0, help_text='安装状态', verbose_name='安装状态'),
        ),
        migrations.CreateModel(
            name='PreInstallHistory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, help_text='创建时间', null=True, verbose_name='创建时间')),
                ('modified', models.DateTimeField(auto_now=True, help_text='更新时间', null=True, verbose_name='更新时间')),
                ('name', models.CharField(default='preInstall', help_text='名称', max_length=32, verbose_name='名称')),
                ('ip', models.GenericIPAddressField(help_text='主机ip地址', verbose_name='主机ip地址')),
                ('install_flag', models.IntegerField(default=0, help_text='0-待安装 1-安装中 2-安装成功 3-安装失败', verbose_name='安装标志')),
                ('install_log', models.TextField(help_text='主机层安装日志', verbose_name='主机层安装日志')),
                ('main_install_history', models.ForeignKey(blank=True, help_text='关联主安装记录', null=True, on_delete=django.db.models.deletion.SET_NULL, to='db_models.maininstallhistory')),
            ],
            options={
                'verbose_name': '前置安装记录',
                'verbose_name_plural': '前置安装记录',
                'db_table': 'omp_pre_install_history',
            },
        ),
    ]