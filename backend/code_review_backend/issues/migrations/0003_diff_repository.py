# -*- coding: utf-8 -*-
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

# Generated by Django 2.2.6 on 2019-11-27 10:23

import django.db.models.deletion
from django.db import migrations
from django.db import models


def _create_diff_repos(apps, schema_editor):
    """
    Initialize the repositories for existing Diff instances
    We currently only have try repositories, so it's easy:
    - a revision on MC has diffs on Try
    - a revision on NSS has diffs on NSS-Try
    """
    Repository = apps.get_model("issues", "Repository")
    Diff = apps.get_model("issues", "Diff")

    # Create try repositories
    repo_try = Repository.objects.create(
        id=100, slug="try", url="https://hg.mozilla.org/try"
    )
    repo_nss_try = Repository.objects.create(
        id=101, slug="nss-try", url="https://hg.mozilla.org/projects/nss-try"
    )

    # MC revisions have diffs on Try
    Diff.objects.filter(revision__repository__slug="mozilla-central").update(
        repository=repo_try
    )

    # NSS revisions have diffs on NSS Try
    Diff.objects.filter(revision__repository__slug="nss").update(
        repository=repo_nss_try
    )


class Migration(migrations.Migration):

    dependencies = [("issues", "0002_compare_issues")]

    operations = [
        migrations.AlterField(
            model_name="repository",
            name="phid",
            field=models.CharField(max_length=40, null=True),
        ),
        migrations.AddField(
            model_name="diff",
            name="repository",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="diffs",
                to="issues.Repository",
            ),
            preserve_default=False,
        ),
        migrations.RunPython(_create_diff_repos),
        migrations.AlterField(
            model_name="diff",
            name="repository",
            field=models.ForeignKey(
                null=False,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="diffs",
                to="issues.Repository",
            ),
            preserve_default=False,
        ),
    ]