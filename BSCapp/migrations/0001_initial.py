# Generated by Django 2.0 on 2018-07-06 01:27

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Admin',
            fields=[
                ('admin_id', models.CharField(max_length=64, primary_key=True, serialize=False)),
                ('admin_name', models.CharField(max_length=20)),
                ('admin_pwd', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Block',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('height', models.IntegerField()),
                ('timestamp', models.CharField(max_length=32)),
                ('block_size', models.FloatField()),
                ('tx_number', models.IntegerField()),
                ('block_hash', models.CharField(max_length=64)),
            ],
        ),
        migrations.CreateModel(
            name='Coin',
            fields=[
                ('coin_id', models.CharField(max_length=64, primary_key=True, serialize=False)),
                ('owner_id', models.CharField(max_length=64)),
                ('is_spent', models.BooleanField(default=False)),
                ('timestamp', models.CharField(max_length=32)),
                ('coin_credit', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='Conference',
            fields=[
                ('article_id', models.CharField(max_length=20, primary_key=True, serialize=False)),
                ('article_name', models.CharField(default='', max_length=400)),
                ('article_authors', models.CharField(default='', max_length=400)),
                ('conference_name', models.CharField(default='', max_length=400)),
                ('keywords', models.CharField(default='', max_length=400)),
                ('abstract', models.CharField(default='', max_length=1000)),
            ],
        ),
        migrations.CreateModel(
            name='Data',
            fields=[
                ('data_id', models.CharField(max_length=64, primary_key=True, serialize=False)),
                ('user_id', models.CharField(max_length=64)),
                ('data_name', models.CharField(max_length=64)),
                ('data_info', models.CharField(max_length=200)),
                ('timestamp', models.CharField(max_length=32)),
                ('data_source', models.CharField(max_length=20)),
                ('data_type', models.CharField(max_length=20)),
                ('data_tag', models.CharField(max_length=100)),
                ('data_status', models.IntegerField(default=0)),
                ('data_md5', models.CharField(max_length=64)),
                ('data_size', models.FloatField()),
                ('data_download', models.IntegerField(default=0)),
                ('data_purchase', models.IntegerField(default=0)),
                ('data_price', models.FloatField()),
                ('data_address', models.CharField(max_length=200)),
                ('data_score', models.FloatField(default=0.0)),
                ('comment_number', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='DataStat',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_title', models.CharField(max_length=64)),
                ('second_title', models.CharField(max_length=64)),
                ('first_number', models.IntegerField(default=0)),
                ('second_number', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Income',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data_id', models.CharField(max_length=64)),
                ('user_name', models.CharField(max_length=20)),
                ('ratio', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='Journal',
            fields=[
                ('article_id', models.CharField(max_length=64, primary_key=True, serialize=False)),
                ('article_name', models.CharField(default='', max_length=400)),
                ('article_authors', models.CharField(default='', max_length=400)),
                ('journal_name', models.CharField(default='', max_length=200)),
                ('keywords', models.CharField(default='', max_length=400)),
                ('abstract', models.CharField(default='', max_length=1000)),
            ],
        ),
        migrations.CreateModel(
            name='Modify',
            fields=[
                ('user_name', models.CharField(max_length=20, primary_key=True, serialize=False, unique=True)),
                ('last_modify_time', models.CharField(max_length=32)),
            ],
        ),
        migrations.CreateModel(
            name='Notice',
            fields=[
                ('notice_id', models.CharField(max_length=64, primary_key=True, serialize=False)),
                ('sender_id', models.CharField(max_length=64)),
                ('receiver_id', models.CharField(max_length=64)),
                ('notice_type', models.IntegerField()),
                ('notice_info', models.CharField(max_length=200)),
                ('if_check', models.BooleanField(default=False)),
                ('timestamp', models.CharField(max_length=32)),
                ('if_delete', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Patent',
            fields=[
                ('patent_id', models.CharField(max_length=20, primary_key=True, serialize=False)),
                ('patent_openId', models.CharField(max_length=64)),
                ('patent_name', models.CharField(max_length=100)),
                ('patent_applicant', models.CharField(max_length=100)),
                ('patent_authors', models.CharField(max_length=200)),
                ('patent_keywords', models.CharField(max_length=400)),
                ('patent_province', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Purchase',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.CharField(max_length=64)),
                ('data_id', models.CharField(max_length=64)),
            ],
        ),
        migrations.CreateModel(
            name='Recharge',
            fields=[
                ('recharge_id', models.CharField(max_length=64, primary_key=True, serialize=False)),
                ('user_id', models.CharField(max_length=64)),
                ('timestamp', models.CharField(max_length=32)),
                ('credits', models.FloatField()),
                ('before_account', models.FloatField()),
                ('after_account', models.FloatField()),
                ('coin_id', models.CharField(max_length=64)),
            ],
        ),
        migrations.CreateModel(
            name='Reset',
            fields=[
                ('user_name', models.CharField(max_length=20, primary_key=True, serialize=False, unique=True)),
                ('secretKey', models.CharField(max_length=64, unique=True)),
                ('last_reset_time', models.CharField(max_length=32)),
            ],
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reviewer_id', models.CharField(max_length=64)),
                ('data_id', models.CharField(max_length=64)),
                ('review_status', models.IntegerField()),
                ('timestamp', models.CharField(max_length=32)),
            ],
        ),
        migrations.CreateModel(
            name='ScienceData',
            fields=[
                ('data_id', models.CharField(max_length=64, primary_key=True, serialize=False)),
                ('user_id', models.CharField(max_length=64)),
                ('user_name', models.CharField(max_length=20)),
                ('timestamp', models.CharField(max_length=64)),
                ('data_name', models.CharField(max_length=64)),
                ('data_source', models.CharField(max_length=64)),
                ('data_info', models.CharField(max_length=90)),
                ('data_type', models.CharField(max_length=64)),
                ('first_title', models.CharField(max_length=64)),
                ('second_title', models.CharField(max_length=64)),
                ('data_address', models.CharField(max_length=200)),
                ('data_status', models.IntegerField(default=0)),
                ('data_size', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('transaction_id', models.CharField(max_length=64, primary_key=True, serialize=False)),
                ('buyer_id', models.CharField(max_length=64)),
                ('seller_id', models.CharField(max_length=64)),
                ('data_id', models.CharField(max_length=64)),
                ('timestamp', models.CharField(max_length=32)),
                ('price', models.FloatField()),
                ('data_score', models.IntegerField(default=0)),
                ('data_comment', models.CharField(default='', max_length=200)),
                ('last_download_time', models.CharField(default='', max_length=32)),
            ],
        ),
        migrations.CreateModel(
            name='TxLog',
            fields=[
                ('TxLog_id', models.CharField(max_length=64, primary_key=True, serialize=False)),
                ('user_id', models.CharField(max_length=64)),
                ('timestamp', models.CharField(max_length=32)),
                ('credits', models.FloatField()),
                ('before_account', models.FloatField()),
                ('after_account', models.FloatField()),
                ('action', models.IntegerField(default=0)),
                ('data_id', models.CharField(max_length=64)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('user_id', models.CharField(max_length=64, primary_key=True, serialize=False)),
                ('user_name', models.CharField(max_length=20, unique=True)),
                ('user_pwd', models.CharField(max_length=20)),
                ('user_email', models.EmailField(max_length=254)),
                ('user_realName', models.CharField(max_length=20)),
                ('user_phone', models.CharField(max_length=20)),
                ('user_idcard', models.CharField(max_length=20)),
                ('user_company', models.CharField(max_length=64)),
                ('user_title', models.CharField(max_length=20)),
                ('user_addr', models.CharField(default='China', max_length=64)),
            ],
        ),
        migrations.CreateModel(
            name='Wallet',
            fields=[
                ('user_id', models.CharField(max_length=64, primary_key=True, serialize=False)),
                ('account', models.FloatField()),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='review',
            unique_together={('reviewer_id', 'data_id')},
        ),
        migrations.AlterUniqueTogether(
            name='purchase',
            unique_together={('user_id', 'data_id')},
        ),
        migrations.AlterUniqueTogether(
            name='income',
            unique_together={('data_id', 'user_name')},
        ),
        migrations.AlterUniqueTogether(
            name='datastat',
            unique_together={('first_title', 'second_title')},
        ),
    ]
