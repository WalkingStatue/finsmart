from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
from django.urls import reverse_lazy
from .forms import TransactionForm
from .forms import DateRangeForm
from django.http import Http404
from .models import Transaction


class UserTransactionsView(LoginRequiredMixin, ListView):
    model = Transaction
    template_name = 'transactions/user_transactions.html'

    def get_queryset(self):
        queryset = Transaction.objects.filter(account__user=self.request.user).order_by('-transaction_date')
        
        # Get the 'start_date' and 'end_date' from the request's GET parameters
        start_date = self.request.GET.get('start_date')
        end_date = self.request.GET.get('end_date')
        
        if start_date and end_date:
            # Filter the queryset based on the provided date range
            queryset = queryset.filter(transaction_date__range=(start_date, end_date))
        
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['date_range_form'] = DateRangeForm(self.request.GET or None)  # Pass initial data to the form
        return context


class TransactionCreateView(LoginRequiredMixin, CreateView):
    model = Transaction
    form_class = TransactionForm
    template_name = 'transactions/transaction_form.html'
    success_url = reverse_lazy('transactions:user_transactions')  # Adjust with the correct URL name

    def form_valid(self, form):
        form.instance.account = self.request.user.account  # Set the account automatically
        return super().form_valid(form)
    
    def get_form_kwargs(self):
        kwargs = super(TransactionCreateView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    


class TransactionUpdateView(LoginRequiredMixin, UpdateView):
    model = Transaction
    form_class = TransactionForm
    template_name = 'transactions/transaction_form.html'

    def get_queryset(self):
        """Ensure the user can only update their own transactions."""
        queryset = super().get_queryset()
        return queryset.filter(account__user=self.request.user)

    def get_success_url(self):
        """Redirect to the transactions list page after a successful update."""
        return reverse_lazy('transactions:user_transactions')


class TransactionDeleteView(LoginRequiredMixin, DeleteView):
    model = Transaction
    template_name = 'transactions/transaction_confirm_delete.html'

    def get_queryset(self):
        """Ensure the user can only delete their own transactions."""
        queryset = super().get_queryset()
        return queryset.filter(account__user=self.request.user)

    def get_success_url(self):
        """Redirect to the transactions list page after a successful deletion."""
        return reverse_lazy('transactions:user_transactions')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        try:
            # Attempt to delete the object and update the wallet balance
            self.object.delete()
            return redirect(self.get_success_url())
        except ValidationError as e:
            # If a ValidationError is raised, return to the previous page and show an error message
            return render(request, 'transactions/transaction_confirm_delete.html', {'error': e.message, 'object': self.object})
