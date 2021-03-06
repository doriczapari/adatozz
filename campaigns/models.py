from django.db import models
from django.utils.translation import ugettext_lazy as _


class Campaign(models.Model):
    name = models.CharField(_("name"), max_length=100)
    created_on = models.DateTimeField(_("created on"), auto_now=True)

    @property
    def completion_rate(self):
        total = self.participants.count()
        completed = self.participants.finished().count()

        if not total:
            return 1

        return completed / total

    @property
    def verification_rate(self):
        total = self.participants.count()
        verified = self.participants.verified().count()

        if not total:
            return 1

        return verified / total

    class Meta:
        verbose_name = _("campaign")
        verbose_name_plural = _("campaigns")

    def __str__(self):
        return self.name


class MPQuerySet(models.QuerySet):
    def finished(self):
        return self.filter(finished=True)

    def unfinished(self):
        return self.filter(finished=False)

    def verified(self):
        return self.filter(verified=True)

    def unverified(self):
        return self.filter(verified=False)


class MP(models.Model):
    campaign = models.ForeignKey('Campaign', verbose_name=_("campaign"), related_name='participants')
    name = models.CharField(_("name"), max_length=200)
    agreement_number = models.PositiveIntegerField(_("agreement number"), blank=True, null=True)
    campaign_start = models.DateField(_("campaign start"), blank=True, null=True)
    campaign_end = models.DateField(_("campaign end"), blank=True, null=True)
    total = models.DecimalField(_("total"), max_digits=10, decimal_places=2, blank=True, null=True)
    signed_on = models.DateField(_("signed on"), blank=True, null=True)
    comment = models.TextField(_("comment"), blank=True)

    pdf_file = models.FileField(_("PDF file"), blank=True)
    finished = models.BooleanField(_("finished"), default=False)
    verified = models.BooleanField(_("verified"), default=False)

    created_on = models.DateTimeField(_("created on"), auto_now_add=True)
    updated_on = models.DateTimeField(_("updated on"), auto_now=True)

    objects = MPQuerySet.as_manager()

    class Meta:
        verbose_name = _("MP")
        verbose_name_plural = _("MPs")

    def __str__(self):
        return self.name


class Expense(models.Model):
    MP = models.ForeignKey('MP', verbose_name=_("MP"))
    row_number = models.PositiveIntegerField(_("row number"))
    invoice_reference = models.CharField(_("invoice reference"), max_length=50)
    delivery_date = models.DateField(_("delivery date"))
    provider = models.CharField(_("provider"), max_length=200)
    product = models.CharField(_("product"), max_length=200)
    purchase_date = models.DateField(_("purchase date"))
    purpose = models.CharField(_("purpose"), max_length=200, blank=True)
    net_amount = models.DecimalField(_("net amount"), max_digits=10, decimal_places=2)
    VAT_amount = models.DecimalField(_("VAT amount"), max_digits=10, decimal_places=2)
    gross_amount = models.DecimalField(_("gross amount"), max_digits=10, decimal_places=2)
    claimed_amount = models.DecimalField(_("claimed amount"), max_digits=10, decimal_places=2)

    class Meta:
        verbose_name = _("expense")
        verbose_name_plural = _("expenses")
