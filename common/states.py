from typing import List
from dataclasses import field
from domain.named_tuple.Topic import Topic
from domain.named_tuple.Contact import Contact
from domain.data_class.Notifications import Notifications


class States:
	SYNTHESIS_WORK = False # Статус работы синтеза речи, для предотвращения коолизий
	WAITING_RESPONSE = False # Статус ожидания ответа на не полную команду
	MUTE = False # Состояние оповещения голосом о новых сообщениях
	WAITING_RESULT_RECOGNITION = True # Ожидание конечного результата распознавания голоса
	ACTION_WITHOUT_FUNCTION = False # Статус вызова комманды с действие, но без функции, которое должно основываться на текущей теме разговора

	TOPIC = Topic() # Текущая тема разговора
	CONTACTS: List[Contact] = field(default_factory=list) # Список контактов
	NOTIFICATIONS = Notifications() # Уведомления которые будут накапливаться и которые можно просматривать и очищать


states = States()