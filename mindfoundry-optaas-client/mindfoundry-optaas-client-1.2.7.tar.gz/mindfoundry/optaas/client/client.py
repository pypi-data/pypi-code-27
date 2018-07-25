from enum import Enum
from typing import List, Any, Dict, TYPE_CHECKING

from mindfoundry.optaas.client.constraint import Constraint
from mindfoundry.optaas.client.parameter import Parameter, GroupParameter
from mindfoundry.optaas.client.session import OPTaaSSession, TASKS_ENDPOINT
from mindfoundry.optaas.client.task import Task

if TYPE_CHECKING:  # pragma: no cover
    from mindfoundry.optaas.client.sklearn_pipelines.mixin import OptimizablePipeline  # pylint: disable=unused-import
    from mindfoundry.optaas.client.sklearn_pipelines.sklearn_task import SklearnTask  # pylint: disable=unused-import


class Goal(Enum):
    """Specifies whether OPTaaS will aim for the lowest (min) or highest (max) score"""
    min = 0
    max = 1


class OPTaaSClient:
    """Sets up a connection to OPTaaS and allows you to create a :class:`.Task`, retrieve existing Tasks etc.

    Args:
        server_url (str): URL of your OPTaaS server
        api_key (str): Your personal API key
        keep_alive (bool, default True): Very rarely required. Set to False only if you experience connection dropping issues.
    """

    def __init__(self, server_url: str, api_key: str, keep_alive: bool = True) -> None:
        self._session = OPTaaSSession(server_url, api_key, keep_alive)

    def create_task(self, title: str, parameters: List[Parameter], constraints: List[Constraint] = None,
                    random_seed: int = None, max_wait_time: float = None, initial_configurations: int = None,
                    goal: Goal = None, target_score: float = None, user_defined_data: Any = None) -> Task:
        """Creates a new :class:`.Task` by making a POST request to OPTaaS

        Args:
            title (str): Name/description of your Task.
            parameters (List[Parameter]): Parameters that you would like to optimize.
            constraints (List[Constraint]): Constraints on what values can be assigned to Parameters.
            goal (Goal, optional, default Goal.max):
                Specify whether OPTaaS should aim for the lowest (min) or highest (max) score
            initial_configurations (int, optional, default 10, minimum 1):
                Number of Configurations that OPTaaS will generate upfront. If you are planning to have multiple clients
                working concurrently, set this to be equal to the number of clients.
            max_wait_time (float, optional, default 5):
                Time (in seconds) to wait for an exploitation configuration to be generated before falling back to exploration.
                See :attr:`.Configuration.type`
            target_score (float, optional):
                Specify (if known) the optimal score value that we want to achieve.
            user_defined_data (Any, optional): Any other data you would like to store in the task JSON
            random_seed (int, optional):
                Seed for the random generator used by OPTaaS when generating :class:`Configurations <.Configuration>`.
                If not specified, a new seed will be used for each Task.
                Use this only if you need reproducible results, i.e. if you create 2 Tasks with identical attributes
                including an identical `random_seed`, and you use the same scoring function, then OPTaaS is guaranteed
                to generate the same Configurations in the same order for both Tasks.

        Returns:
            A new :class:`.Task`

        Raises:
            :class:`.OPTaaSError` if the Task data is invalid or the server is unavailable.
        """
        body: Dict = dict(
            title=title,
            parameters=[p.to_json() for p in parameters],
            constraints=[constraint.to_optaas_expression() for constraint in constraints] if constraints else [],
            goal=goal.name if goal else None,
            randomSeed=random_seed,
            userDefined=user_defined_data,
            initialConfigurations=initial_configurations,
            maxWaitTime=max_wait_time,
            targetScore=target_score
        )
        body = {key: value for key, value in body.items() if value is not None}
        response = self._session.post(TASKS_ENDPOINT, body=body)
        return Task(json=response.body, session=self._session)

    def create_sklearn_task(self, title: str, pipeline: 'OptimizablePipeline',
                            additional_parameters: List[Parameter] = None,
                            additional_constraints: List[Constraint] = None,
                            random_seed: int = None, max_wait_time: float = None, initial_configurations: int = None,
                            goal: Goal = None, target_score: float = None, user_defined_data: Any = None,
                            **kwargs) -> 'SklearnTask':
        """Creates a new :class:`.SklearnTask` by making a POST request to OPTaaS

        All the arguments from :meth:`.OPTaaSClient.create_task` can be used here except instead of
        `parameters` and `constraints` there is `additional_parameters` and `additional_constraints`.

        Args:
            pipeline (OptimizablePipeline): The pipeline you wish to optimize.
            additional_parameters (List[Parameter], optional):
                Additional parameters that you would like to optimize.
            additional_constraints (List[Constraint], optional):
                Additional constraints on your Parameters.
            kwargs:
                Additional arguments required to optimize certain estimators, e.g. :class:`.PCA` requires `feature_count`.

        Returns:
            A new :class:`.SklearnTask`

        Raises:
            :class:`.MissingArgumentError` if a required argument is missing from `kwargs`.
            :class:`.OPTaaSError` if the Task data is invalid or the server is unavailable.
        """
        from mindfoundry.optaas.client.sklearn_pipelines.sklearn_task import SklearnTask  # pylint: disable=redefined-outer-name

        parameters, constraints = pipeline.make_all_parameters_and_constraints('pipeline', '', **kwargs)

        if additional_parameters:
            parameters.append(GroupParameter('additional', items=additional_parameters))
        if additional_constraints:
            constraints.extend(additional_constraints)

        task = self.create_task(title=title, parameters=parameters, constraints=constraints,
                                random_seed=random_seed, max_wait_time=max_wait_time, goal=goal,
                                initial_configurations=initial_configurations, target_score=target_score,
                                user_defined_data=user_defined_data)
        return SklearnTask(task, pipeline.estimators)

    def get_all_tasks(self) -> List[Task]:
        """Retrieves a list of all stored Tasks by making a GET request to OPTaaS.

        Returns:
            List of :class:`Tasks <.Task>`

        Raises:
            :class:`.OPTaaSError` if the server is unavailable
        """
        response = self._session.get(TASKS_ENDPOINT)
        return [Task(json, self._session) for json in response.body['tasks']]

    def get_task(self, task_id: str) -> Task:
        """Retrieves a stored :class:`.Task` by making a GET request to OPTaaS.

        Args:
            task_id (str): unique id for the Task

        Returns:
            A :class:`.Task`

        Raises:
            :class:`.OPTaaSError` if no record is found with the given id or the server is unavailable.
        """
        response = self._session.get(f'{TASKS_ENDPOINT}/{task_id}')
        return Task(response.body, self._session)

    def get_sklearn_task(self, task_id: str, pipeline: 'OptimizablePipeline') -> 'SklearnTask':
        """Retrieves a stored :class:`.SklearnTask` by making a GET request to OPTaaS.

        This allows you to create a SklearnTask and then use it again in a separate/later session, assuming of course
        that you call this method with the same `estimators` you used to create the original task.

        Args:
            task_id (str): unique id for the Task
            pipeline (OptimizablePipeline): The same pipeline used when calling :meth:`.OPTaaSClient.create_sklearn_task`

        Returns:
            A :class:`.SklearnTask`

        Raises:
            :class:`.OPTaaSError` if no record is found with the given id or the server is unavailable.
        """
        from mindfoundry.optaas.client.sklearn_pipelines.sklearn_task import SklearnTask  # pylint: disable=redefined-outer-name
        task = self.get_task(task_id)
        return SklearnTask(task, pipeline.estimators)
