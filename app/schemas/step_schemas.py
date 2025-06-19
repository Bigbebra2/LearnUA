from pydantic import BaseModel, Field, HttpUrl, ConfigDict
from typing import Annotated, Literal


# Common types
list_options = Annotated[list[Annotated[str, Field(min_length=1, max_length=256)]], Field(min_length=2, max_length=10)]


class SingleOptionModel(BaseModel):
    model_config = ConfigDict(
        json_schema_extra={
            'examples': [{
                'question': 'how much is 1 + 1?',
                'options': [
                    '3', '2', 'bro, idk!'
                ],
                'answer': '2'
            }]
        }
    )

    question: Annotated[str, Field(min_length=5, max_length=512)]
    options: list_options
    answer: Annotated[str, Field(min_length=1, max_length=256)]


class MultipleOptionModel(SingleOptionModel):
    model_config = ConfigDict(
        json_schema_extra={
            'examples': [{
                'question': 'Which of the following is a fruit?',
                'options': [
                    'apple', 'potato', 'pear', 'cucumber', 'grape'
                ],
                'answer': ['apple', 'pear', 'grape']
            }]
        }
    )
    answer: list_options


class OrderedQuizInput(SingleOptionModel):
    model_config = ConfigDict(
        json_schema_extra={
            'examples': [{
                'question': 'In what order are the seasons?',
                'options': [
                     'spring', 'winter', 'fall', 'summer'
                ],
                'answer': {'winter': 1, 'spring': 2, 'summer': 3, 'fall': 4}
            }]
        }
    )
    answer: Annotated[dict[str, int], Field(min_length=2, max_length=15)]



class VideoModel(BaseModel):
    model_config = ConfigDict(
        json_schema_extra={
            'examples': [{
                'content_type': 'video',
                'video_url': 'https://www.youtube.com/watch?v=KWtwIf-TSlo'
            }]
        }
    )
    content_type: Literal['video']
    video_url: HttpUrl


class SingleQuestionModel(BaseModel):
    content_type: Literal['single_question']
    quiz_data: SingleOptionModel

    model_config = ConfigDict(
        json_schema_extra={'examples': [
            {'content_type': 'single_question',
             'quiz_data': SingleOptionModel.model_json_schema().get('examples')[0]
             }
        ]}
    )


class MultipleQuestionChoiceModel(BaseModel):
    content_type: Literal['multiple_question_choice']
    quiz_data: MultipleOptionModel

    model_config = ConfigDict(
        json_schema_extra={'examples': [
            {'content_type': 'multiple_question_choice',
             'quiz_data': MultipleOptionModel.model_json_schema().get('examples')[0]}
        ]}
    )


class OrderQuizModel(BaseModel):
    content_type: Literal['order_quiz']
    quiz_data: OrderedQuizInput
    model_config = ConfigDict(
        json_schema_extra={'examples': [
            {'content_type': 'order_quiz',
             'quiz_data': OrderedQuizInput.model_json_schema().get('examples')[0]}
        ]}
    )


class StepIn(BaseModel):

    title: Annotated[str, Field(min_length=2)]
    model: (VideoModel | SingleQuestionModel
            | MultipleQuestionChoiceModel | OrderQuizModel) = Field(
        discriminator='content_type'
    )
    model_config = ConfigDict(
        json_schema_extra={
            'examples': [
                {
                    'title': 'some title, min length = 2',
                    'model': VideoModel.model_json_schema().get('examples')[0],
                },
                {
                    'title': 'some title, min length = 2',
                    'model': SingleQuestionModel.model_json_schema().get('examples')[0],
                },
                {
                    'title': 'some title, min length = 2',
                    'model': MultipleQuestionChoiceModel.model_json_schema().get('examples')[0],
                },
                {
                    'title': 'some title, min length = 2',
                    'model': OrderQuizModel.model_json_schema().get('examples')[0]
                }
            ]
        }, extra='allow'
    )


class StepQuery(BaseModel):
    step_place: int

class SectionQuery(BaseModel):
    course_id: int

class LessonQuery(BaseModel):
    course_id: int
    section_place: int