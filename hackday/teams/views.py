from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.generic import CreateView
from django.views.generic import DetailView
from django.views.generic import ListView
from django.views.generic import UpdateView

from teams.forms import CreateTeamForm
from teams.forms import UpdateTeamForm
from teams.models import STATUS
from teams.models import Team
from teams.models import TeamCreateStatus

from assets.models import Attachment
from assets.models import ImageAttachment
from assets.models import Link
from assets.forms import AttachmentForm
from assets.forms import ImageAttachmentForm
from assets.forms import LinkAttachmentForm

class TeamListView(ListView):
    model = Team
    queryset = Team.objects.filter(status=STATUS.ACTIVE)


class TeamDetailView(DetailView):
    model = Team
    queryset = Team.objects.filter(status=STATUS.ACTIVE)


class TeamUpdateView(UpdateView):
    model = Team
    form_class = UpdateTeamForm
    queryset = Team.objects.filter(status=STATUS.ACTIVE)

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        """ If user isn't a team member (or team isn't active),
            redirect to team listing.
        """
        try:
            response = super(TeamUpdateView, self).dispatch(*args, **kwargs)
        except:
            return HttpResponseRedirect(reverse('teams-list'))
        if not self.object.is_member(self.request.user):
            return HttpResponseRedirect(reverse('teams-list'))
        return response

    def form_valid(self, form):
        """ In case the user forgets, add the captain as a team member.
        """
        team = form.save()
        team.add_captain_as_member()

        return HttpResponseRedirect(reverse('teams-detail',
            kwargs={'slug': team.slug}))


class TeamCreateView(CreateView):
    model = Team
    form_class = CreateTeamForm

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        """ If team creation is disabled (via admin), redirect.
        """
        try:
            online = TeamCreateStatus.objects.all()[0].online
        except:
            online = True

        if online:
            return super(CreateView, self).dispatch(*args, **kwargs)
        else:
            return render(args[0], 'teams/create_offline.html');

    def form_valid(self, form):
        """ Because team doesn't exist in DB yet, and creator is required,
            we need to first save the form, add creator, and THEN save to DB
        """
        team = form.save(commit=False)
        team.status = STATUS.ACTIVE
        team.creator = self.request.user
        team.save()
        form.save_m2m()
        team.add_captain_as_member()

        return HttpResponseRedirect(reverse('teams-detail',
            kwargs={'slug': team.slug}))


def delete(request, slug):
    try:
        team = Team.objects.get(slug=slug)
        if team.is_member(request.user):
            team.status = STATUS.DELETED
            team.save()
            return HttpResponseRedirect(reverse('teams-list'))
        else:
            return HttpResponseRedirect(reverse('teams-detail',
                kwargs={'slug': slug}))
    except:
        return HttpResponseRedirect(reverse('teams-detail',
            kwargs={'slug': slug}))


def upload_attachment(request, slug):
    env = {}

    team = Team.objects.get(slug=slug)
    if not team.is_member(request.user):
        return HttpResponseRedirect(reverse('teams-detail',
            kwargs={'slug': slug}))

    if request.method == 'POST':
        form = AttachmentForm(request.POST, request.FILES)
        if form.is_valid():
            attachment = Attachment(attached_file = form.cleaned_data['attached_file'],
                                   title = form.cleaned_data['title'],
                                   alt_text = form.cleaned_data['alt_text'])
            attachment.save()
            team.attachments.add(attachment)
            return HttpResponseRedirect(reverse('teams-detail',
                kwargs={'slug': slug}))
    else:
        form = AttachmentForm()

    env['form'] = form
    return render(request, 'teams/upload.html', env)


def remove_attachment(request, slug, attachment_id):
    team = Team.objects.get(slug=slug)
    if team.is_member(request.user):
        attachment = Attachment.objects.get(id=attachment_id)
        team.attachments.remove(attachment)

    return HttpResponseRedirect(reverse('teams-detail',
        kwargs={'slug': slug}))


def upload_image(request, slug):
    env = {}

    team = Team.objects.get(slug=slug)
    if not team.is_member(request.user):
        return HttpResponseRedirect(reverse('teams-detail',
            kwargs={'slug': slug}))

    if request.method == 'POST':
        form = ImageAttachmentForm(request.POST, request.FILES)
        if form.is_valid():
            image = ImageAttachment(attached_file = form.cleaned_data['attached_file'],
                                    title = form.cleaned_data['title'],
                                    alt_text = form.cleaned_data['alt_text'])
            image.save()
            team.images.add(image)
            return HttpResponseRedirect(reverse('teams-detail',
                kwargs={'slug': slug}))
    else:
        form = ImageAttachmentForm()

    env['form'] = form
    return render(request, 'teams/upload.html', env)


def remove_image(request, slug, attachment_id):
    team = Team.objects.get(slug=slug)
    if team.is_member(request.user):
        image = ImageAttachment.objects.get(id=attachment_id)
        team.images.remove(image)

    return HttpResponseRedirect(reverse('teams-detail',
        kwargs={'slug': slug}))


def add_link(request, slug):
    env = {}

    team = Team.objects.get(slug=slug)
    if not team.is_member(request.user):
        return HttpResponseRedirect(reverse('teams-detail',
            kwargs={'slug': slug}))

    if request.method == 'POST':
        form = LinkAttachmentForm(request.POST)
        if form.is_valid():
            link = Link(url = form.cleaned_data['url'],
                        title = form.cleaned_data['title'],
                        text = form.cleaned_data['text'])
            link.save()
            team.links.add(link)
            return HttpResponseRedirect(reverse('teams-detail',
                kwargs={'slug': slug}))
    else:
        form = LinkAttachmentForm()

    env['form'] = form
    return render(request, 'teams/upload.html', env)


def remove_link(request, slug, attachment_id):
    team = Team.objects.get(slug=slug)
    if team.is_member(request.user):
        link = LinkAttachment.objects.get(id=attachment_id)
        team.links.remove(link)

    return HttpResponseRedirect(reverse('teams-detail',
        kwargs={'slug': slug}))
