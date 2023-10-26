import torch
from transformers import BertForSequenceClassification
import numpy as np

model = BertForSequenceClassification.from_pretrained("bert-base-uncased",num_labels=4,output_attentions = False,output_hidden_states = False)
model.load_state_dict(torch.load('bert-fine-tuning/fine_tuned_model.pt',map_location=torch.device('cpu') ))
model.eval()

# model.predict("I love you")

from transformers import BertTokenizer

# Load the BERT tokenizer.
print('Loading BERT tokenizer...')
tokenizer = BertTokenizer.from_pretrained('bert-base-uncased', do_lower_case=True)
input_ids = []
attention_masks = []
encoded_dict = tokenizer.encode_plus(
                        "The bot was stupid and it didn't reply my message, just hang there",                      # Sentence to encode.
                        add_special_tokens = True, # Add '[CLS]' and '[SEP]'
                        max_length = 512,           # Pad & truncate all sentences.
                        truncation = True,
                        padding = 'max_length',
                        return_attention_mask = True,   # Construct attn. masks.
                        return_tensors = 'pt',     # Return pytorch tensors.
                   )
 # Add the encoded sentence to the list.
input_ids.append(encoded_dict['input_ids'])

# And its attention mask (simply differentiates padding from non-padding).
attention_masks.append(encoded_dict['attention_mask'])
input_ids = torch.cat(input_ids, dim=0)
attention_masks = torch.cat(attention_masks, dim=0)

outputs = model(input_ids,
                            token_type_ids=None,
                            attention_mask=attention_masks)

issuetypes = ['content-clarity', 'enquiries-account', 
       'technical-service unavailable', 
       'technical-logging-authentication-token',
      ]
print(outputs.logits.detach().cpu().numpy().tolist())
predicted = outputs.logits.detach().cpu().numpy().tolist()[0]
print(predicted)
print(np.argmax(predicted))
print(f'Label: {issuetypes[np.argmax(predicted)]}')