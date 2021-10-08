# Generated by Django 3.1.4 on 2021-10-08 20:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('db_models', '0008_auto_20210929_1411'),
    ]

    operations = [
        migrations.CreateModel(
            name='Labels',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label_name', models.CharField(help_text='标签名称', max_length=16, verbose_name='标签名称')),
                ('label_type', models.IntegerField(choices=[(0, '服务'), (1, '应用')], default=0, help_text='标签类型', verbose_name='标签类型')),
            ],
            options={
                'verbose_name': '应用产品标签表',
                'verbose_name_plural': '应用产品标签表',
                'db_table': 'omp_labels',
            },
        ),
        migrations.CreateModel(
            name='UploadPackageHistory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, help_text='创建时间', null=True, verbose_name='创建时间')),
                ('modified', models.DateTimeField(auto_now=True, help_text='更新时间', null=True, verbose_name='更新时间')),
                ('operation_uuid', models.CharField(help_text='唯一操作uuid', max_length=64, verbose_name='唯一操作uuid')),
                ('operation_user', models.CharField(blank=True, help_text='操作用户', max_length=64, null=True, verbose_name='操作用户')),
                ('package_name', models.CharField(help_text='安装包名称', max_length=256, verbose_name='安装包名称')),
                ('package_md5', models.CharField(help_text='安装包MD5值', max_length=64, verbose_name='安装包MD5值')),
                ('package_path', models.CharField(help_text='安装包路径', max_length=512, verbose_name='安装包路径')),
                ('package_status', models.IntegerField(choices=[(0, '成功'), (1, '失败'), (2, '解析中')], default=2, help_text='安装包状态', verbose_name='安装包状态')),
                ('error_msg', models.CharField(blank=True, help_text='错误消息', max_length=1024, null=True, verbose_name='错误消息')),
                ('package_parent', models.ForeignKey(blank=True, help_text='父级包', null=True, on_delete=django.db.models.deletion.SET_NULL, to='db_models.uploadpackagehistory')),
            ],
            options={
                'verbose_name': '上传安装包记录',
                'verbose_name_plural': '上传安装包记录',
                'db_table': 'omp_upload_package_history',
            },
        ),
        migrations.CreateModel(
            name='ProductHub',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, help_text='创建时间', null=True, verbose_name='创建时间')),
                ('modified', models.DateTimeField(auto_now=True, help_text='更新时间', null=True, verbose_name='更新时间')),
                ('is_release', models.BooleanField(default=False, help_text='是否发布', verbose_name='是否发布')),
                ('pro_name', models.CharField(help_text='产品名称', max_length=256, verbose_name='产品名称')),
                ('pro_version', models.CharField(help_text='产品版本', max_length=256, verbose_name='产品版本')),
                ('pro_description', models.CharField(blank=True, help_text='产品描述', max_length=2048, null=True, verbose_name='产品描述')),
                ('pro_dependence', models.TextField(blank=True, help_text='产品依赖', null=True, verbose_name='产品依赖')),
                ('pro_services', models.TextField(blank=True, help_text='服务列表', null=True, verbose_name='服务列表')),
                ('pro_logo', models.TextField(blank=True, help_text='产品图标', null=True, verbose_name='产品图标')),
                ('extend_fields', models.JSONField(blank=True, help_text='冗余字段', null=True, verbose_name='冗余字段')),
                ('pro_labels', models.ManyToManyField(help_text='所属标签', to='db_models.Labels')),
                ('pro_package', models.ForeignKey(blank=True, help_text='安装包', null=True, on_delete=django.db.models.deletion.SET_NULL, to='db_models.uploadpackagehistory', verbose_name='安装包')),
            ],
            options={
                'verbose_name': '应用商店产品',
                'verbose_name_plural': '应用商店产品',
                'db_table': 'omp_product',
            },
        ),
        migrations.CreateModel(
            name='ApplicationHub',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, help_text='创建时间', null=True, verbose_name='创建时间')),
                ('modified', models.DateTimeField(auto_now=True, help_text='更新时间', null=True, verbose_name='更新时间')),
                ('is_release', models.BooleanField(default=False, help_text='是否发布', verbose_name='是否发布')),
                ('app_type', models.IntegerField(choices=[(0, '组件'), (1, '服务')], default=0, help_text='应用类型', verbose_name='应用类型')),
                ('app_name', models.CharField(help_text='应用名称', max_length=256, verbose_name='应用名称')),
                ('app_version', models.CharField(help_text='应用版本', max_length=256, verbose_name='应用版本')),
                ('app_description', models.CharField(blank=True, help_text='应用描述', max_length=2048, null=True, verbose_name='应用描述')),
                ('app_port', models.TextField(blank=True, help_text='应用端口', null=True, verbose_name='应用端口')),
                ('app_dependence', models.TextField(blank=True, help_text='应用依赖', null=True, verbose_name='应用依赖')),
                ('app_install_args', models.TextField(blank=True, help_text='安装参数', null=True, verbose_name='安装参数')),
                ('app_controllers', models.TextField(blank=True, help_text='应用控制脚本', null=True, verbose_name='应用控制脚本')),
                ('app_logo', models.TextField(blank=True, help_text='应用图标', null=True, verbose_name='应用图标')),
                ('extend_fields', models.JSONField(blank=True, help_text='冗余字段', null=True, verbose_name='冗余字段')),
                ('app_labels', models.ManyToManyField(help_text='所属标签', to='db_models.Labels')),
                ('app_package', models.ForeignKey(blank=True, help_text='安装包', null=True, on_delete=django.db.models.deletion.SET_NULL, to='db_models.uploadpackagehistory', verbose_name='安装包')),
                ('product', models.ForeignKey(blank=True, help_text='所属产品', null=True, on_delete=django.db.models.deletion.SET_NULL, to='db_models.producthub', verbose_name='所属产品')),
            ],
            options={
                'verbose_name': '应用商店服务',
                'verbose_name_plural': '应用商店服务',
                'db_table': 'omp_application',
            },
        ),
    ]
